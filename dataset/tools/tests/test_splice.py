"""The launch splicer's entry spans on a library text with an anchored entry (9.13 D4: `game-download` carries a YAML
anchor so `game-download-idle` can merge it)."""

from meas.campaign import splice

TEXT = (
    "archetypes:\n"
    "  file-archiver:\n"
    "    category_source: meas\n"
    "    declared_class: normal\n"
    "\n"
    "  game-download: &game-download\n"
    "    category_source: meas\n"
    "    declared_class: normal\n"
    "\n"
    "  game-download-idle:\n"
    "    <<: *game-download\n"
    "    declared_class: idle\n"
    "\n"
    "  package-upgrade:\n"
    "    category_source: meas\n"
)


def test_blocks_see_an_anchored_entry_as_its_own_block():
    spans = splice.blocks(TEXT)
    assert list(spans) == ["file-archiver", "game-download", "game-download-idle", "package-upgrade"]
    a, b = spans["file-archiver"]
    assert TEXT[a:b] == "  file-archiver:\n    category_source: meas\n    declared_class: normal\n\n"
    a, b = spans["game-download"]
    assert TEXT[a:b].startswith("  game-download: &game-download\n") and "<<:" not in TEXT[a:b]
