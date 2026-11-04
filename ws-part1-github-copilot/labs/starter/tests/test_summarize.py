import subprocess
import sys
from pathlib import Path

import pytest

from summarize import load_rows, summarize


DATA = Path(__file__).resolve().parents[1] / "data"


def test_load_sales():
    rows = load_rows(DATA / "sales.csv")
    assert len(rows) == 4
    assert rows[0] == {"region": "East", "amount": "100"}


def test_load_rows_trims_region_names(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\n  East  ,100\n", encoding="utf-8")

    assert load_rows(path) == [{"region": "East", "amount": "100"}]


def test_zero_amount_is_valid(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\nEast,0\n", encoding="utf-8")

    assert summarize(load_rows(path)) == ({"East": 0.0}, 0.0)


@pytest.mark.parametrize(
    ("path", "message"),
    [
        (DATA / "invalid-amount.csv", "line 3: amount must be numeric"),
        (DATA / "missing-column.csv", "missing required columns: amount"),
    ],
)
def test_supplied_invalid_csv_files_raise_useful_errors(path, message):
    with pytest.raises(ValueError, match=message):
        load_rows(path)


def test_blank_region_is_rejected_with_line_number(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\n   ,10\n", encoding="utf-8")

    with pytest.raises(ValueError, match="line 2: region must not be blank"):
        load_rows(path)


@pytest.mark.parametrize("amount", ["nan", "inf", "-inf"])
def test_nonfinite_amount_is_rejected_with_line_number(tmp_path, amount):
    path = tmp_path / "sales.csv"
    path.write_text(f"region,amount\nEast,{amount}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="line 2: amount must be finite"):
        load_rows(path)


def test_negative_amount_is_rejected_with_line_number(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("region,amount\nEast,-1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="line 2: amount must be nonnegative"):
        load_rows(path)


def test_zero_byte_csv_reports_missing_columns(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_rows(path)


@pytest.mark.parametrize(
    ("row", "message"),
    [
        ("East", "line 2: malformed row has too few fields"),
        ("East,10,extra", "line 2: malformed row has too many fields"),
        ('East,"10', "line 2: malformed CSV"),
    ],
)
def test_malformed_rows_are_rejected_with_line_number(tmp_path, row, message):
    path = tmp_path / "sales.csv"
    path.write_text(f"region,amount\n{row}\n", encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        load_rows(path)


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


def test_invalid_csv_from_command_line_has_no_partial_report():
    result = run_report(str(DATA / "invalid-amount.csv"))

    assert result.returncode != 0
    assert result.stdout == ""
    assert "line 3: amount must be numeric" in result.stderr
    assert "Traceback" not in result.stderr


def test_missing_column_from_command_line_has_no_partial_report():
    result = run_report(str(DATA / "missing-column.csv"))

    assert result.returncode != 0
    assert result.stdout == ""
    assert "missing required columns: amount" in result.stderr
    assert "Traceback" not in result.stderr


def test_default_command_line_report_is_unchanged():
    result = run_report(str(DATA / "sales.csv"))

    assert result.returncode == 0
    assert result.stdout == (
        "East: 150.00\nNorth: 75.00\nWest: 250.00\n"
        "Average per region: 158.33\n"
    )
    assert result.stderr == ""
