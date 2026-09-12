# tests

The pytest suite for the harness, the hand-written fixtures it checks the code against, and the two mocks that stand in for the daemon and the simulator.

```
python3 -m pytest tools/tests -q        # from harness/; or make test
```

About 250 tests in 90 seconds. A handful drive the runner end to end on the mocks over compiled coreset files and are skipped when `dataset/build/coreset-single` is absent; build it with `make -C ../dataset dataset` to run them.

## How the suite is built

Almost every number the code produces is checked against a value computed by hand first. `fixtures/` holds the hand-written inputs and their expected outputs: six mock trace pairs with their records, hand-written records with their aggregates and scores, hand-written recognition logs with their records and grades, and a per-experiment spec in three variants with its expected reports. Each fixture's `worked.md` shows the arithmetic. `fixtures/README.md` describes every fixture.

The tests then come in three kinds:

- **Reproduction tests** assert that a command reproduces an expected file byte for byte. These are the ground truth for the pipeline; when a rule changes, the fixture's expectation and its worked derivation change with it, in the same commit.
- **Rule tests** take a fixture, break one thing, and assert the refusal or the changed value: a trace out of time order, a spec pin that does not match, a guard input that is missing.
- **Pinning tests** hold two things equal that live in different trees and must not drift: the harness's driver-table composition against the daemon's, the OSTEP boot default against the config schema's defaults, the mock daemon's graded set against the count the 8.4 spec measured.

`conftest.py` puts `tools/` on the path so tests import `harness` and the mocks directly, and names the fixture directories.

## Mocks

`mocks/` holds the mock daemon and the mock simulator, each a library module plus a command that speaks the invocation contract. They are what `make smoke` and the runner tests invoke, and they are discarded when the real programs land. [mocks/README.md](mocks/README.md).
