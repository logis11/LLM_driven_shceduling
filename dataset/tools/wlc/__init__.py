"""wlc — workload compiler: timeline + archetypes.yaml -> canonical workload.

Contract: docs/simulator/interpretation-contract.md (canonical semantics),
_dev/docs/spec/task-2.3-timeline-compiler.md (format + tooling decisions),
dataset/schema/workload.schema.json (output shape).
"""

from .units import parse_us
from .library import Library
from .timeline import Timeline, TimelineError
from .compiler import compile_timeline
from .estimate import demand_estimate
