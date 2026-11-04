import argparse
import csv
import math

REQUIRED_COLUMNS = ("region", "amount")


class CsvInputError(ValueError):
    """Raised when the sales CSV is not valid input."""


def validate_row(row: dict, line: int) -> dict[str, str]:
    if None in row or any(value is None for value in row.values()):
        raise CsvInputError(f"line {line}: malformed row (wrong number of fields)")
    region = row["region"].strip()
    if not region:
        raise CsvInputError(f"line {line}: region must not be blank")
    amount = row["amount"].strip()
    try:
        value = float(amount)
    except ValueError:
        raise CsvInputError(f"line {line}: invalid amount {amount!r}") from None
    if not math.isfinite(value) or value < 0:
        raise CsvInputError(
            f"line {line}: amount must be a finite, nonnegative number, got {amount!r}"
        )
    return {"region": region, "amount": amount}


def load_rows(path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise CsvInputError("file is empty; expected header 'region,amount'")
        missing = [name for name in REQUIRED_COLUMNS if name not in reader.fieldnames]
        if missing:
            raise CsvInputError(
                f"line 1: missing required column(s): {', '.join(missing)}"
            )
        return [validate_row(row, reader.line_num) for row in reader]


def summarize(rows):
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + float(row["amount"])
    average = sum(totals.values()) / len(totals) if totals else 0.0
    return totals, average


def top_region(totals: dict[str, float]) -> tuple[str, float]:
    """Return the region with the largest total, breaking ties alphabetically."""
    return min(totals.items(), key=lambda item: (-item[1], item[0]))


def main():
    parser = argparse.ArgumentParser(description="Summarize sales by region.")
    parser.add_argument("path", help="Path to the sales CSV")
    parser.add_argument("--region", help="Filter the report to one region")
    args = parser.parse_args()
    try:
        rows = load_rows(args.path)
        if args.region is not None:
            rows = [row for row in rows if row["region"] == args.region]
            if not rows:
                parser.exit(2, f"Error: unknown region: {args.region}\n")
        totals, average = summarize(rows)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"Error: {error}\n")
    for region, amount in sorted(totals.items()):
        print(f"{region}: {amount:.2f}")
    print(f"Average per region: {average:.2f}")


if __name__ == "__main__":
    main()
