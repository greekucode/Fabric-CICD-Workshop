import subprocess
import sys
from pathlib import Path

import pytest

from summarize import CsvInputError, load_rows, summarize


STARTER = Path(__file__).resolve().parents[1]
DATA = STARTER / "data"


def run_report(*args):
    return subprocess.run(
        [sys.executable, str(STARTER / "summarize.py"), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def write_csv(tmp_path, content: str, name: str = "input.csv") -> Path:
    path = tmp_path / name
    path.write_bytes(content.encode("utf-8"))
    return path


def assert_rejected(result, *fragments):
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("Error:") or "Error:" in result.stderr
    for fragment in fragments:
        assert fragment in result.stderr


def test_invalid_amount_fixture():
    result = run_report(str(DATA / "invalid-amount.csv"))
    assert_rejected(result, "line 3", "not-a-number")


def test_missing_column_fixture():
    result = run_report(str(DATA / "missing-column.csv"))
    assert_rejected(result, "line 1", "amount")


def test_blank_region_is_rejected(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10\n   ,5\n")
    assert_rejected(run_report(str(path)), "line 3", "blank")


def test_region_whitespace_is_trimmed(tmp_path):
    path = write_csv(tmp_path, "region,amount\n East ,10\nEast,5\n")
    assert load_rows(path) == [
        {"region": "East", "amount": "10"},
        {"region": "East", "amount": "5"},
    ]
    totals, _ = summarize(load_rows(path))
    assert totals == {"East": 15.0}


def test_zero_amount_is_allowed(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,0\nWest,10\n")
    result = run_report(str(path))
    assert result.returncode == 0
    assert result.stdout == "East: 0.00\nWest: 10.00\nAverage per region: 5.00\n"
    assert result.stderr == ""


@pytest.mark.parametrize("amount", ["-1", "-0.01"])
def test_negative_amount_is_rejected(tmp_path, amount):
    path = write_csv(tmp_path, f"region,amount\nEast,{amount}\n")
    assert_rejected(run_report(str(path)), "line 2", "nonnegative")


@pytest.mark.parametrize("amount", ["nan", "inf", "-inf", "Infinity"])
def test_nonfinite_amount_is_rejected(tmp_path, amount):
    path = write_csv(tmp_path, f"region,amount\nEast,10\nWest,{amount}\n")
    assert_rejected(run_report(str(path)), "line 3", "finite")


def test_blank_amount_is_rejected(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,\n")
    assert_rejected(run_report(str(path)), "line 2", "invalid amount")


def test_zero_byte_file_is_rejected(tmp_path):
    path = write_csv(tmp_path, "")
    assert_rejected(run_report(str(path)), "empty")


def test_short_row_is_rejected(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10\nWest\n")
    assert_rejected(run_report(str(path)), "line 3", "malformed")


def test_extra_field_row_is_rejected(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10,extra\n")
    assert_rejected(run_report(str(path)), "line 2", "malformed")


def test_unterminated_quote_is_rejected_without_traceback(tmp_path):
    path = write_csv(tmp_path, 'region,amount\n"East,10\n', "quote.csv")
    result = run_report(str(path))
    assert result.returncode != 0
    assert result.stdout == ""
    assert "Traceback" not in result.stderr


def test_missing_file_is_reported_without_traceback(tmp_path):
    result = run_report(str(tmp_path / "absent.csv"))
    assert_rejected(result)


def test_invalid_row_never_produces_partial_stdout(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10\nWest,oops\n")
    assert run_report(str(path)).stdout == ""


def test_load_rows_raises_csv_input_error(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,-5\n")
    with pytest.raises(CsvInputError, match="line 2"):
        load_rows(path)


def test_region_filter_still_works_with_validation(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10\nWest,20\n")
    result = run_report(str(path), "--region", "West")
    assert result.returncode == 0
    assert result.stdout == "West: 20.00\nAverage per region: 20.00\n"


def test_region_filter_does_not_skip_invalid_rows(tmp_path):
    path = write_csv(tmp_path, "region,amount\nEast,10\nWest,oops\n")
    assert_rejected(run_report(str(path), "--region", "East"), "line 3")
