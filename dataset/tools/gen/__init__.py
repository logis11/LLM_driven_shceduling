"""gen — the generated layer's generator (9.19 spec): the grid definition (`dataset/grids.yaml`) and the sixteen C1
task sets composed into one timeline per cell, which the workload compiler then compiles like any other timeline.

cells.py    the definition, the modes, the 240 ordered pairs, each set's cells with keyed seeds and splits
compose.py  one cell -> one timeline (9.10 D44's placement; the batch jobs scaled to their span)
"""

from .cells import cells, lint_grids, load_definition, modes_of, ordered_pairs, seed_of
from .compose import c1_sets, compose
