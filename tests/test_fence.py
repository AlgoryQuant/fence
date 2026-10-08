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
