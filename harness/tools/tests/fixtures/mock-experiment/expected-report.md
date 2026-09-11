# Report — mock-experiment

**Verdict: pass** — 1 of 1 judging files met the criterion (K = 1). Spec `71736b062545`.

## Criterion

| field | value |
|---|---|
| type | k_of_n_gap |
| k | 1 |
| g | 0.500000 |
| reference | oracle |
| compared | random |
| seed_statistic | mean |

## Pins

| pin | path | sha256 | version |
|---|---|---|---|
| scoring_spec | harness/tools/tests/fixtures/mock-scores/scoring-spec.yaml | da3b9f9c4adb9a75f195925abe49d0a24ad690f2333b27df383cb8012c82e1fb |  |
| guard_spec | harness/tools/tests/fixtures/mock-experiment/guard-spec.yaml | 40bdfb01dd8bbfc451ebf3ee84d9f1d48b641400f01eb38fbe64b088212f9fb0 | 0.1 |
| driver_table | harness/tools/tests/fixtures/mock-grades/driver-table.yaml | 04fdb608c64661905af94f1a01e5502f5f84f004cd4c433b9297fc284c99f3de |  |
| dataset | harness/tools/tests/fixtures/mock-experiment/build.manifest.json | b60942339c09f9ea6155bdac98c293a8184de082f4fd95f1b9134dee98bdd44f |  |

## Per-file gaps

| workload | judging | boot default | reference | compared (per seed) | mean | gap | meets g | no headroom | random beats oracle | available |
|---|---|---|---|---|---|---|---|---|---|---|
| mock-score | True | (primary) | 2.500000 | s1: 1.639359, s2: 0.433333 | 1.036346 | 0.585462 | True | 1/4 | False | True |
| mock-score | True | alt | 2.500000 | s1: 1.533876, s2: 0.210172 | 0.872024 | 0.651190 | True | 1/4 | False | True |

## Line: sensitivity

| boot default | met | judging | verdict | available |
|---|---|---|---|---|
| (primary) | 1 | 1 | pass | True |
| alt | 1 | 1 | pass | True |

## Line: floor_band

| latency floor (µs) | met | judging | verdict |
|---|---|---|---|
| 500 | 1 | 1 | pass |
| 1000 | 1 | 1 | pass |
| 40000 | 0 | 1 | fail |

| latency floor (µs) | workload | reference | mean | gap | meets g | all no headroom |
|---|---|---|---|---|---|---|
| 500 | mock-score | 2.500000 | 1.036346 | 0.585462 | True | False |
| 1000 | mock-score | 2.500000 | 1.036346 | 0.585462 | True | False |
| 40000 | mock-score | 2.500000 | 2.175000 | 0.130000 | False | False |

## Line: exclusion_accuracy

| condition | table | axis | statistic | excluded (headline) | included | n excluded | n included |
|---|---|---|---|---|---|---|---|
| oracle | prior | attribute | balanced_accuracy | 1.000000 | 1.000000 | 2 | 4 |
| oracle | prior | mode | raw_accuracy | 1.000000 | 1.000000 | 2 | 4 |
| random | prior | attribute | balanced_accuracy | 0.750000 | 0.625000 | 2 | 4 |
| random | prior | mode | raw_accuracy | 0.500000 | 0.375000 | 2 | 4 |

## Line: layer1_headline

| condition | table | balanced accuracy | CI | n | files | seeds |
|---|---|---|---|---|---|---|
| oracle | prior | 1.000000 |  | 2 | 1 | 1 |
| random | prior | 0.750000 |  | 2 | 1 | 2 |

Confusion, attribute, oracle (prior):

| seed | truth | predicted | count |
|---|---|---|---|
| (one) | true | false | 0 |
| (one) | true | true | 2 |

Confusion, attribute, random (prior):

| seed | truth | predicted | count |
|---|---|---|---|
| s1 | true | false | 1 |
| s1 | true | true | 1 |
| s2 | true | false | 0 |
| s2 | true | true | 2 |

## Line: random_beats_oracle

| workload | flagged | gap |
|---|---|---|
| mock-score | False | 0.585462 |

## Line: note

**mock-score** — A pre-registered note bound to the judging file, shown beside its row.

## Guards

28 pass, 1 fail, 11 not applicable.

| run | guard | value | threshold | reason | exempt | invalidating |
|---|---|---|---|---|---|---|
| mock-score · random · s2 | starvation_floor | 1500000.000000000000 | 1000000.000000000000 | train: max ready_wait 1500000 exceeds 1000000 | The fixture's random s2 run starves `train` by construction; the exemption keeps the pass variant judgeable (worked.md). | False |

## Provenance breakdown

| run | unmodified | clamped | held | fallback | fallback share |
|---|---|---|---|---|---|
| mock-score · fixed | 0.000000000000 | 0.000000000000 | 0.000000000000 | 1.000000000000 | 1.000000000000 |
| mock-score · fixed · boot alt | 0.000000000000 | 0.000000000000 | 0.000000000000 | 1.000000000000 | 1.000000000000 |
| mock-score · oracle | 1.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| mock-score · random · s1 | 1.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| mock-score · random · s2 | 1.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |

## Scores

| run | scored against | score | weight sum | terms | no headroom | censored |
|---|---|---|---|---|---|---|
| mock-score · fixed | (primary) | 0.500000 | 2.500000 | 4 | 1 | 0 |
| mock-score · fixed | alt | 0.500000 | 2.500000 | 4 | 1 | 0 |
| mock-score · oracle | (primary) | 2.500000 | 2.500000 | 4 | 1 | 0 |
| mock-score · oracle | alt | 2.500000 | 2.500000 | 4 | 1 | 0 |
| mock-score · random · s1 | (primary) | 1.639359 | 2.500000 | 4 | 1 | 0 |
| mock-score · random · s1 | alt | 1.533876 | 2.500000 | 4 | 1 | 0 |
| mock-score · random · s2 | (primary) | 0.433333 | 2.500000 | 4 | 1 | 1 |
| mock-score · random · s2 | alt | 0.210172 | 2.500000 | 4 | 1 | 1 |
