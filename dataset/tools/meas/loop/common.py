"""Shared pieces of the campaign loop (_dev/research/jioh/measurement-campaign-workflow.md): the campaign families,
GitHub run and job queries, job states, the machine-gate reading of an artifact, and the trigger-file push.

Run from the repository root on the development machine. Downloads go under the work directory — $MEAS_LOOP_WORK,
default ~/.cache/meas-loop — which lives outside the repository and survives a reboot.
"""

import datetime
import json
import os
import re
import subprocess

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
WORK = os.environ.get("MEAS_LOOP_WORK", os.path.expanduser("~/.cache/meas-loop"))
MACHINE = "EPYC 7763"   # 9.6 D10-D11: the one CPU model of every campaign
GATE_S = 120            # a job that finished sooner measured nothing: the machine gate stopped it, or it failed early
SCOPE = os.environ.get("MEAS_LOOP_SCOPE", "jioh/phase-9")   # the conventional-commit scope of the trigger pushes

# A family is one workflow and its trigger file. Families with apps name jobs "run (<app>, <k>)" and artifacts
# meas-<family>-<app>-r<k>-<mode>; the build family names them "run (<k>)" and meas-build-r<k>-<mode>.
FAMILIES = {
    "interactive": {"workflow": "meas-interactive.yml", "trigger": ".github/campaign.json", "apps": True,
                    "pool": "dataset/tools/meas/campaign/pool.py"},
    "playback": {"workflow": "meas-playback.yml", "trigger": ".github/campaign.json", "apps": True,
                 "pool": "dataset/tools/meas/campaign/pool.py"},
    "build": {"workflow": "meas-build.yml", "trigger": ".github/campaign-build.json", "apps": False,
              "pool": "dataset/tools/meas/build/pool.py"},
    "background": {"workflow": "meas-background.yml", "trigger": ".github/campaign-background.json", "apps": True,
                   "pool": "dataset/tools/meas/background/pool.py"},
    # 9.5 D35, D42: a long-phase probe of one application's steady phase — never a campaign repeat, so no pool
    "long-probe": {"workflow": "meas-long-probe.yml", "trigger": ".github/campaign-long-probe.json", "apps": True,
                   "pool": None},
}


def parse_target(s):
    """'interactive/code:18' -> ('interactive', 'code', 18); 'build:9' -> ('build', None, 9); a missing ':k' -> k None."""
    head, _, k = s.partition(":")
    fam, _, app = head.partition("/")
    if fam not in FAMILIES:
        raise SystemExit(f"unknown family {fam!r} (one of {', '.join(FAMILIES)})")
    return fam, (app or None), (int(k) if k else None)


def gh(*args):
    out = subprocess.run(["gh", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return json.loads(out) if out.strip() else None


def runs(family, since=1):
    """The family's runs numbered `since` or later, oldest first."""
    rs = gh("run", "list", "--workflow", FAMILIES[family]["workflow"], "-L", "300", "--json", "databaseId,number,status")
    return sorted((r for r in rs if r["number"] >= since), key=lambda r: r["number"])


def _t(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def run_jobs(run_id):
    """The run's jobs as gh reports them; a completed run's list never changes, so it is kept under the work directory
    and not asked for again (each pool and each watcher pass reads every run since N: 2026-09-19, the account's API
    rate limit was reached with ~150 runs read a pool)."""
    cache = os.path.join(WORK, "jobs", f"{run_id}.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    data = gh("run", "view", str(run_id), "--json", "jobs,status") or {}
    if data.get("status") == "completed":
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        json.dump(data, open(cache, "w"))
    return data


def jobs(family, run_id):
    """The run's measurement jobs as dicts: app (None for build), k, state, seconds."""
    out = []
    for j in run_jobs(run_id).get("jobs", []):
        m = re.fullmatch(r"run \((?:(.+), )?(\d+)\)", j["name"])
        if not m or j.get("conclusion") == "skipped":
            continue
        if j["status"] != "completed":
            state, secs = ("measuring" if j["status"] == "in_progress" else "queued"), None
        else:
            secs = (_t(j["completedAt"]) - _t(j["startedAt"])).total_seconds()
            state = "failed" if j["conclusion"] != "success" else ("short" if secs < GATE_S else "landed")
        out.append({"run": run_id, "app": m.group(1), "k": int(m.group(2)), "state": state, "seconds": secs, "name": j["name"]})
    return out


def mode(family):
    return json.load(open(os.path.join(REPO, FAMILIES[family]["trigger"]))).get("mode", "full")


def artifact(family, app, k):
    m = mode(family)
    return f"meas-build-r{k}-{m}" if family == "build" else f"meas-{family}-{app}-r{k}-{m}"


def artifact_names(run_id):
    """The names of a run's artifacts (a dry check's are meas-build-r<k>-dry, never a repeat of a full campaign)."""
    return [a["name"] for a in (gh("api", f"repos/{{owner}}/{{repo}}/actions/runs/{run_id}/artifacts") or {}).get("artifacts", [])]


def download(run_id, name, dest):
    """One artifact into its own folder (gh extracts an -n download flat)."""
    if os.path.exists(os.path.join(dest, "report.json")):
        return dest
    os.makedirs(dest, exist_ok=True)
    subprocess.run(["gh", "run", "download", str(run_id), "-n", name, "-D", dest], cwd=REPO, capture_output=True, check=True)
    return dest


def gate_of(family, job):
    """(gate, machine.model) from the job's report.json — 'wrong-machine' when the machine gate stopped it."""
    d = download(job["run"], artifact(family, job["app"], job["k"]),
                 os.path.join(WORK, "gate", str(job["run"]), f"{job['app'] or 'build'}-r{job['k']}"))
    try:
        r = json.load(open(os.path.join(d, "report.json")))
    except (OSError, ValueError):
        return None, None
    return r.get("gate"), r.get("machine.model")


def push_trigger(targets, kind, dry=False):
    """Write the trigger file(s) for the given (family, app, k) targets, commit and push. kind: first | added | retried | probe.
    Every family of a shared trigger file that is not named gets apps [] so the push starts nothing there."""
    by_trigger = {}
    for fam, app, k in targets:
        by_trigger.setdefault(FAMILIES[fam]["trigger"], []).append((fam, app, k))
    for trig, ts in by_trigger.items():
        p = os.path.join(REPO, trig)
        d = json.load(open(p))
        d["attempt"] = d.get("attempt", 0) + 1
        if trig.endswith("campaign-build.json"):
            d["repeats"] = sorted(k for _, _, k in ts)
        elif trig.endswith(("campaign-background.json", "campaign-long-probe.json")):
            m = {}
            for _, app, k in ts:
                m.setdefault(app, []).append(k)
            d["apps"], d["repeats"] = sorted(m), {a: sorted(w) for a, w in sorted(m.items())}
        else:
            for fam in ("interactive", "playback"):
                m = {}
                for f, app, k in ts:
                    if f == fam:
                        m.setdefault(app, []).append(k)
                d[fam] = {"apps": sorted(m), "repeats": {a: sorted(w) for a, w in m.items()}}
        d["cpu_model"] = MACHINE
        if not dry:
            open(p, "w").write(json.dumps(d, indent=2) + "\n")
    what = ", ".join(f"{app or 'repeat'} {k}" for _, app, k in targets)
    why = {"first": "first batch launched", "added": "repeat added — the stability rule does not hold yet",
           "retried": "gated windows retried", "probe": "long-phase probe launched, not a repeat (9.5 D35, D42)"}[kind]
    msg = f"chore({SCOPE}): campaign — {why} ({what})"
    if dry:
        return msg
    git = lambda *a: subprocess.run(["git", *a], cwd=REPO, check=True, capture_output=True, text=True)
    git("add", *by_trigger)
    git("commit", "-q", "-m", msg)
    git("pull", "-q", "--rebase", "--autostash")
    git("push", "-q")
    return msg
