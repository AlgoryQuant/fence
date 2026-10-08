from pathlib import Path

import fence

ROOT = Path(__file__).resolve().parents[1]


def test_ok_diff_stays_inside_the_implement_card():
    card = (ROOT / "cards" / "implement.md").read_text(encoding="utf-8")
    diff = (ROOT / "samples" / "ok.diff").read_text(encoding="utf-8")
    assert fence.check(card, diff) is None


def test_bad_diff_reports_the_readme():
    card = (ROOT / "cards" / "implement.md").read_text(encoding="utf-8")
    diff = (ROOT / "samples" / "bad.diff").read_text(encoding="utf-8")
    assert fence.check(card, diff) == "README.md"


def test_rejected_samples_match_the_eval_table():
    card = (ROOT / "cards" / "implement.md").read_text(encoding="utf-8")
    expected = {
        "escape.diff": "src/../README.md",
        "cards.diff": "cards/implement.md",
        "outside.diff": "../secrets.env",
        "empty.diff": "diff has no files",
    }
    for name, problem in expected.items():
        diff = (ROOT / "samples" / name).read_text(encoding="utf-8")
        assert fence.check(card, diff) == problem


def test_a_card_without_a_forbid_line_does_not_allow_every_path():
    assert fence.check("Role: open.\n", "diff --git a/src/fence.py b/src/fence.py\n") == (
        "card has no May not write line"
    )


def test_cli_exits_zero_for_the_ok_sample():
    code = fence.main(
        [
            "check",
            "--card",
            str(ROOT / "cards" / "implement.md"),
            "--diff",
            str(ROOT / "samples" / "ok.diff"),
        ]
    )
    assert code == 0
