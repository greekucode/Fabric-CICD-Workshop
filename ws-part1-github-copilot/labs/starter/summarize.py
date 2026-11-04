import argparse
import csv
import math
from pathlib import Path


def load_rows(path: str | Path) -> list[dict[str, str]]:
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source, strict=True)
        try:
            fieldnames = reader.fieldnames
            missing_columns = {"region", "amount"} - set(fieldnames or [])
            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(f"CSV is missing required columns: {missing}")

            for row in reader:
                line_number = reader.line_num
                if None in row:
                    raise ValueError(
                        f"line {line_number}: malformed row has too many fields"
                    )
                if any(value is None for value in row.values()):
                    raise ValueError(
                        f"line {line_number}: malformed row has too few fields"
                    )

                region = row["region"].strip()
                if not region:
                    raise ValueError(f"line {line_number}: region must not be blank")

                try:
                    amount = float(row["amount"])
                except ValueError as error:
                    raise ValueError(
                        f"line {line_number}: amount must be numeric"
                    ) from error
                if not math.isfinite(amount):
                    raise ValueError(
                        f"line {line_number}: amount must be finite"
                    )
                if amount < 0:
                    raise ValueError(
                        f"line {line_number}: amount must be nonnegative"
                    )

                row["region"] = region
                rows.append(row)
        except csv.Error as error:
            raise ValueError(
                f"line {reader.line_num + 1}: malformed CSV: {error}"
            ) from error
    return rows


def summarize(rows: list[dict[str, str]]) -> tuple[dict[str, float], float]:
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + float(row["amount"])
    average = sum(totals.values()) / len(totals)
    return totals, average


def top_region(totals: dict[str, float]) -> tuple[str, float]:
    """Return the region with the largest total, breaking ties alphabetically."""
    return min(totals.items(), key=lambda item: (-item[1], item[0]))


def main() -> None:
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
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    for region, amount in sorted(totals.items()):
        print(f"{region}: {amount:.2f}")
    print(f"Average per region: {average:.2f}")


if __name__ == "__main__":
    main()
