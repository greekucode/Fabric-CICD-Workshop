import subprocess
import sys
from pathlib import Path

from summarize import load_rows, summarize


DATA = Path(__file__).resolve().parents[1] / "data"


def test_load_sales():
    rows = load_rows(DATA / "sales.csv")
    assert len(rows) == 4
    assert rows[0] == {"region": "East", "amount": "100"}


def test_totals_by_region():
    totals, _ = summarize(load_rows(DATA / "sales.csv"))
    assert totals == {"East": 150.0, "West": 250.0, "North": 75.0}


def test_average_is_mean_of_regional_totals():
    _, average = summarize(load_rows(DATA / "sales.csv"))
    assert average == 475 / 3


def run_report(*args):
    script = Path(__file__).resolve().parents[1] / "summarize.py"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_region_filter_from_command_line():
    result = run_report(str(DATA / "sales.csv"), "--region", "East")

    assert result.returncode == 0
    assert result.stdout == "East: 150.00\nAverage per region: 150.00\n"
    assert result.stderr == ""


def test_unknown_region_from_command_line():
    result = run_report(str(DATA / "sales.csv"), "--region", "east")

    assert result.returncode != 0
    assert result.stdout == ""
    assert "unknown region: east" in result.stderr


def test_default_command_line_report_is_unchanged():
    result = run_report(str(DATA / "sales.csv"))

    assert result.returncode == 0
    assert result.stdout == (
        "East: 150.00\nNorth: 75.00\nWest: 250.00\n"
        "Average per region: 158.33\n"
    )
    assert result.stderr == ""
