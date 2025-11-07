
import csv
from pathlib import Path
import sys

CSV_PATH = Path(".github/workflows/Resources Data Stewardship - git.csv")       # change if your CSV path differs
OUTPUT = Path("resources-table.md")
START = "<!-- AUTO-TABLE:START -->"
END = "<!-- AUTO-TABLE:END -->"

def csv_to_markdown_table(csv_path, max_rows=None):
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if not reader:
        return "_No data_"
    headers = reader[0]
    rows = reader[1:]
    if max_rows:
        rows = rows[:max_rows]

    # header row
    md = ["|" + "|".join(h if h else " " for h in headers) + "|"]
    # alignment row (left align)
    md.append("|" + "|".join("---" for _ in headers) + "|")
    # data rows
    for r in rows:
        md.append("|" + "|".join((c or " ").replace("\n", " ") for c in r) + "|")
    return "\n".join(md)

def replace_between_markers(text, start, end, replacement):
    if start not in text or end not in text:
        raise SystemExit(f"Markers not found in OUTPUT: {start} / {end}")
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    return f"{pre}{start}\n\n{replacement}\n\n{end}{post}"

def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV not found: {CSV_PATH}")
    md_table = csv_to_markdown_table(CSV_PATH, max_rows=None)
    original = OUTPUT.read_text(encoding="utf-8")
    updated = replace_between_markers(original, START, END, md_table)
    if updated != original:
        OUTPUT.write_text(updated, encoding="utf-8")
        print("OUTPUT updated.")
    else:
        print("No changes.")

if __name__ == "__main__":
    sys.exit(main())
