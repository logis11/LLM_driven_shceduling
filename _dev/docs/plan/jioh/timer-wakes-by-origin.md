# Plan — timer wakes by origin

Spec: `_dev/docs/spec/jioh/timer-wakes-by-origin.md` (12 decisions, 2026-10-31). Data: `_dev/research/jioh/2026-10-31-wake-origins/`. Worked on `main` in small commits; 인경민 receives the decisions and the simulator's part in `docs/memos/2026-10-30-harness-changes-for-the-simulator.md`, updated in place.

## Stages

1. [ ] Measurement tools, interactive family (`dataset/tools/meas/campaign/`): `analyze.py` gives each wake the origin of its chain (the X server relaying, the harness and GIMP's Script-Fu server as input); `pool.py` keys a component by its channel and applies D16's coverage cut per channel; `fold_in.py` writes `channel: event` on the event parts. Tests in `dataset/tools/tests/`.
2. [ ] Raw files: the releases each pooled record reads (interactive 2026-09-18, -19 with -28, -20, -25, -27; the Kdenlive idle campaign 2026-10-05; the launch subjects 2026-10-04b, -10-05, -10-05b), each asset's SHA-256 against `dataset/meas-releases.yaml`.
3. [ ] Re-pool and re-fold: the pooled records under `_dev/research/jioh/task-9.5-interactive-typing/campaign/` and `task-9.10-…/kdenlive-idle/` regenerated; the nine entries re-spliced into `dataset/archetypes.yaml`, the regeneration test byte for byte.
4. [ ] Streams: launch streams (`dataset/launch/`) and wake-kind replay streams (`dataset/replay/`) carry each wake's channel; heavy events by their origin.
5. [ ] Desktop and session families (question 13, pending): the same for `renderer-hidden`, `chat-client`, `game-client` and the session daemons.
6. [ ] Compiler and workload schema: `event:` channel; a component's `channel`; the TIMER description to the skip rule.
7. [ ] Rebuild and re-bless: core set, variants, generated layer; manifests; RQ0 gate spec pins.
8. [ ] Harness: reader (`event:` wakes, `wake_drop` lines); `app_latency` in place of `timer_latency`; records schema; aggregates and scorer; scoring spec re-frozen; guard spec 1.4; the mock simulator and fixtures; tests.
9. [ ] Contracts and docs: interpretation contract, data contracts (§4, §9, §14), simulator guide, metrics doc, RQ0 gate spec (a conformance item for the two channels, re-pin), harness CHANGELOG, a verified source for queued messages, guidebooks and guides where they state the timer channel.
10. [ ] Memo to 인경민 updated in place, written out in full: every decision and the simulator's part.
