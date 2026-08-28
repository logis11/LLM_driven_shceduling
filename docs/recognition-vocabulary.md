# Recognition Vocabulary
> Status: normative · Created 2026-08-28 · Updated 2026-08-28

The shared vocabulary of the recognition signal — the one list that the recognizer's output schema, the validator's menu, the driver table's input axis, and the Layer-1 grader all agree on. Ratified 2026-08-28 (인지오 · 인경민 · 박이안 — pending team review of this doc). The vocabulary is identical to the dataset's ground-truth labels: recognizer answers and ground truth are compared directly, with no mapping layer.

These labels were not invented for this doc — they come out of the dataset itself. Every mode below appears as a segment label in the released coreset, and each labeled segment carries `scenario` tags keying it to the scenario catalog (`workload/scenario-catalog.md`), whose co-occurrence patterns are grounded in cited sources — desktop-usage taxonomies, workload-benchmark suites, and our own CI measurements — resolvable through `references.md`. The same holds for `background_wanted`: it is the intent axis the C2 pair files were authored around. Adopting the dataset's labels as the vocabulary therefore means every term the recognizer can answer is backed by the citations that justified authoring a workload for it.

## Modes

A **mode** is the label for what the machine is primarily being used for during a segment. The recognizer answers exactly one mode per query, from this closed menu of 16:

| Mode | The machine is being used for |
|---|---|
| `browsing` | web browsing as the main activity |
| `office` | documents, spreadsheets, presentations |
| `mail` | reading and writing email |
| `dev` | writing code in an editor/IDE |
| `photo` | photo editing |
| `meeting` | a live video call |
| `gaming` | playing a game in the foreground |
| `media` | media playback (video, music) |
| `video-edit` | interactive video editing |
| `compile` | building software |
| `ml-train` | a machine-learning training run |
| `render` | an offline 3D/graphics render |
| `transcode` | batch media conversion |
| `indexing` | file indexing / crawling |
| `backup` | a backup job |
| `idle` | no human present; maintenance only |

### `ambiguous` — ground truth only

Ground-truth segments may carry the label `ambiguous` (equally-active dual foregrounds — the C6 boundary case). It is **not on the recognizer menu**: a recognizer must always commit to one of the 16, and `ambiguous` segments are excluded from accuracy scoring and reported separately as a scope boundary.

## Attributes

One graded attribute:

- **`background_wanted`** (boolean) — *is the sustained background work something the user asked for?* `true` for work the user deliberately initiated or is waiting on (a download, a kicked-off training run, a render); `false` for work nobody asked for right now (a scheduled scan, an indexer's rescan). **Convention: when a segment has no sustained background work at all, `background_wanted` is `true`** — nothing unwanted is running — keeping the attribute a plain boolean.

## Ground-truth annotations (never recognizer-facing)

Ground-truth segments may carry additional descriptive keys used for grading splits and failure analysis only: `background` (what the background work is, e.g. `download`, `av-scan`), `initiated` (`user` | `scheduled`), `dual_active`, `spoof`. They are not part of the recognizer's output schema, not on the validator's menu, and not graded.

## The recognizer output schema

The machine-readable core of every proposal:

```jsonc
"system": {
  "mode": "ml-train",          // exactly one of the 16
  "background_wanted": true    // boolean, always present
}
```

The validator rejects any answer whose `mode` is not on the menu, whose `background_wanted` is missing or non-boolean, or which carries any other key inside `system`.

## Extension rule

Adding or removing a mode, promoting an annotation to a graded attribute, or changing an attribute's semantics is an all-three decision, recorded here with a changelog entry and a statement of its re-labeling and re-grading impact.
