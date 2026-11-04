import argparse
import csv


def load_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as source:
        return list(csv.DictReader(source))


def summarize(rows):
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + float(row["amount"])
    average = sum(totals.values()) / len(totals)
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
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    for region, amount in sorted(totals.items()):
        print(f"{region}: {amount:.2f}")
    print(f"Average per region: {average:.2f}")


if __name__ == "__main__":
    main()
