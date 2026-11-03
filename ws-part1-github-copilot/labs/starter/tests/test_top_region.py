import pytest

from summarize import top_region


def test_top_region():
    assert top_region({"East": 150.0, "West": 250.0, "North": 75.0}) == (
        "West",
        250.0,
    )


def test_top_region_tie_breaks_alphabetically():
    assert top_region({"West": 250.0, "East": 250.0}) == ("East", 250.0)


def test_top_region_with_no_totals():
    with pytest.raises(ValueError):
        top_region({})
