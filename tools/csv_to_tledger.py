import csv
import sys
from datetime import datetime
from pathlib import Path


def parse_date(date_str):
    return datetime.strptime(date_str.strip(), "%m/%d/%Y")


def format_date(dt):
    return dt.strftime("%Y-%m-%d")


def load_csv(filepath):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return fieldnames, rows


def get_month(rows):
    months = {parse_date(row["date"]).strftime("%Y-%m") for row in rows}
    if len(months) > 1:
        sys.exit(f"Error: CSV contains multiple months: {', '.join(sorted(months))}")
    return months.pop()


def row_to_lines(row, metric_columns):
    date_str = format_date(parse_date(row["date"]))
    lines = []
    for col in metric_columns:
        value = row[col].strip()
        if value:
            lines.append(f"{date_str} {col.lower()} {value}")
    return lines


def convert(filepath):
    fieldnames, rows = load_csv(filepath)
    metric_columns = [f for f in fieldnames if f.lower() != "date"]
    month = get_month(rows)

    output_lines = []
    for row in rows:
        output_lines.extend(row_to_lines(row, metric_columns))

    output_path = Path(filepath).parent / f"{month}.txt"
    output_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print(f"Written {len(output_lines)} lines to {output_path}")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python csv_to_long.py <path/to/file.csv>")
    convert(sys.argv[1])


if __name__ == "__main__":
    main()