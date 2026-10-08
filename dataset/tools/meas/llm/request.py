#!/usr/bin/env python3
"""Time recognizer-shaped requests against a running llama-server (9.12 latency campaign, research-slice changelog
D31).

The chat is prompt.json's system and user messages, formatted by the server's own chat template
(`POST /apply-template`); each request is `POST /completion` with that prompt, a JSON schema constraining the
answer (schema.system.json — the `system` block alone; schema.full.json — `reasoning` and `situation` before it,
the proposal's order), temperature 0, a fixed seed and `cache_prompt` false, so every request evaluates the whole
prompt. One untimed-for-the-pool warm-up request first, then the two schemas alternated. Per request: the wall
time from send to the full response, the server's `timings` (prompt and generation, tokens and ms), the stop type,
the answer, whether it parses and the mode it names.

    request.py <url> <dir of prompt.json and schemas> <requests per schema>   → JSON lines on stdout
"""

import json
import os
import sys
import time
import urllib.request


def post(url, body, timeout=600):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.load(resp)
    return data, (time.perf_counter() - t0) * 1000.0


def main(url, here, n):
    p = json.load(open(os.path.join(here, "prompt.json")))
    schemas = {k: json.load(open(os.path.join(here, f"schema.{k}.json"))) for k in ("system", "full")}
    msgs = [{"role": "system", "content": p["system"]}, {"role": "user", "content": p["user"]}]
    templ, _ = post(url + "/apply-template", {"messages": msgs})
    prompt = templ["prompt"]
    print(json.dumps({"kind": "template", "prompt_chars": len(prompt), "prompt": prompt}), flush=True)
    order = [("warmup", "system")] + [(f"r{i}", k) for i in range(1, n + 1) for k in ("system", "full")]
    for label, k in order:
        body = {"prompt": prompt, "n_predict": 384, "temperature": 0, "seed": 1, "cache_prompt": False,
                "json_schema": schemas[k]}
        data, wall = post(url + "/completion", body)
        content = data.get("content", "")
        try:
            ans = json.loads(content)
            mode, ok = ans.get("system", {}).get("mode"), True
        except ValueError:
            mode, ok = None, False
        print(json.dumps({"kind": "request", "label": label, "schema": k, "wall_ms": round(wall, 3),
                          "timings": data.get("timings"), "tokens_evaluated": data.get("tokens_evaluated"),
                          "tokens_predicted": data.get("tokens_predicted"), "stop_type": data.get("stop_type"),
                          "parses": ok, "mode": mode, "content": content}), flush=True)


if __name__ == "__main__":
    main(sys.argv[1].rstrip("/"), sys.argv[2], int(sys.argv[3]))
