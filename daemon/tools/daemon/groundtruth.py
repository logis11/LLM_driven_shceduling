"""The answer key — for the oracle recognizer and nothing else.

`ground_truth` (data-contracts §4) is the labelled interval list a canonical
workload was built from. Reading it is exactly what the oracle condition is
*for* (daemon-guide §4), and exactly what every other condition must be unable
to do. The isolation is structural: this is the only module that touches the
key, `projection.py` does not import it, and `tests/test_isolation.py` fails
the build if anything outside the oracle's allowlist starts to.

Two properties of the key that the oracle has to live with, both from
recognition-vocabulary §1:

  * a segment's `mode` may be `ambiguous`, which is *not* on the recognizer's
    16-mode menu (c6-dual). This reader returns it as it stands. Deciding what
    the oracle emits there is deferred past RQ0 and is not this module's call —
    but the reader must not raise, because a lookup that dies on an off-menu
    mode would kill a 24-file sweep at its last stage.
  * `attributes` may lack `background_wanted` for the same reason, so it is
    returned as given and never defaulted. Substituting a value here would put
    our judgment into the oracle's answer, which is the one thing the oracle
    must not contain.

`familiarity` is carried because it is a reporting split key for the grader;
it is not part of any answer.
"""

import json
from dataclasses import dataclass
from typing import Mapping, Optional, Tuple

from .errors import GroundTruthError


@dataclass(frozen=True)
class Segment:
    """One labelled interval, half-open `[t_start, t_end)`."""

    t_start: int
    t_end: int
    mode: str
    attributes: Mapping[str, object]
    familiarity: Optional[int] = None

    def covers(self, t_us):
        return self.t_start <= t_us < self.t_end


@dataclass(frozen=True)
class GroundTruth:
    """A workload's answer key, sorted by `t_start`."""

    workload_id: str
    segments: Tuple[Segment, ...]

    def covering(self, t_us):
        """The segment covering `t_us`, or None.

        None is a real answer, not a failure: the terminal snapshot every
        coreset file emits (data-contracts §5, rule 4) lands at the workload's
        end, where no segment covers it, and the grader skips it. Callers
        handle None; this never raises.
        """
        for segment in self.segments:
            if segment.covers(t_us):
                return segment
        return None


def _time(value, path, what):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise GroundTruthError(f"{path}: {what} must be a non-negative integer "
                               f"microsecond value, got {value!r}")
    return value


def read_ground_truth(path):
    """Read a canonical workload file's answer key. Oracle-only — see module
    docstring before importing this anywhere new."""
    try:
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
    except OSError as exc:
        raise GroundTruthError(f"{path}: cannot be opened ({exc.strerror})") from exc
    except json.JSONDecodeError as exc:
        raise GroundTruthError(f"{path}: not JSON ({exc})") from exc

    if not isinstance(document, dict) or "ground_truth" not in document:
        raise GroundTruthError(f"{path}: not a canonical workload file "
                               f"(no ground_truth)")
    meta = document.get("meta")
    workload_id = meta.get("id") if isinstance(meta, dict) else None
    if not isinstance(workload_id, str) or not workload_id:
        raise GroundTruthError(f"{path}: meta.id is missing or not a string")

    raw = document["ground_truth"]
    if not isinstance(raw, list) or not raw:
        raise GroundTruthError(f"{path}: ground_truth is empty or not a list")

    segments = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise GroundTruthError(f"{path}: ground_truth[{index}] is not an object")
        mode = item.get("mode")
        if not isinstance(mode, str) or not mode:
            raise GroundTruthError(f"{path}: ground_truth[{index}] has no mode")
        t_start = _time(item.get("t_start"), path, f"ground_truth[{index}].t_start")
        t_end = _time(item.get("t_end"), path, f"ground_truth[{index}].t_end")
        if t_end <= t_start:
            raise GroundTruthError(f"{path}: ground_truth[{index}] ends at {t_end}, "
                                   f"at or before its start {t_start}")
        attributes = item.get("attributes", {})
        if not isinstance(attributes, dict):
            raise GroundTruthError(f"{path}: ground_truth[{index}].attributes "
                                   f"is not an object")
        segments.append(Segment(t_start=t_start, t_end=t_end, mode=mode,
                                attributes=dict(attributes),
                                familiarity=item.get("familiarity")))

    segments.sort(key=lambda s: s.t_start)
    return GroundTruth(workload_id=workload_id, segments=tuple(segments))
