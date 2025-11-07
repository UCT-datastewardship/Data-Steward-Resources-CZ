import csv
from pathlib import Path
import sys

CSV_PATH = Path(".github/workflows/Resources Data Stewardship - git.csv")                # <--- change if needed
OUTPUT_FILE = Path("resources-table.md")        # <--- where table goes
START = "<!-- AUTO-TABLE:START -->"
END = "<!-- AUTO-TABLE:END -->"

def ensure_output_file_has_markers(path: Path):
    if not path.exists():
        path.write_text(
            "# 📊 Data Steward Resources Table\n\n"
            f"{START}\n{END}\n",
            encoding="utf-8",
        )
        print(f"Created {path} with markers.")
    else:
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            # Append markers if missing
            with path.open("a", encoding="utf-8") as f:
                if not text.endswith("\n"):
                    f.write("\n")
                f.write(f"\n{START}\n{END}\n")
            print(f"Added markers to {path} (they were missing).")

def read_csv_rows(csv_path: Path):
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path.resolve()}")
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    return reader

def csv_to_markdown_table(rows, max_rows=None):
    if not rows:
        return "_No data_"
    headers = rows[0]
    data = rows[1:]
    if max_rows:
        data = data[:max_rows]
    # If there are no data rows, still render headers with an empty row
    md = ["|" + "|".join(h if h else " " for h in headers) + "|"]
    md.append("|" + "|".join("---" for _ in headers) + "|")
    if data:
        for r in data:
            md.append("|" + "|".join((c or " ").replace("\n", " ") for c in r) + "|")
    else:
        md.append("|" + "|".join(" " for _ in headers) + "|")
    return "\n".join(md)

def replace_between_markers(text, start, end, replacement):
    if start not in text or end not in text:
        raise SystemExit("Markers not found in output file.")
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    return f"{pre}{start}\n\n{replacement}\n\n{end}{post}"

def main():
    print(f"Output file: {OUTPUT_FILE.resolve()}")
    print(f"CSV path:    {CSV_PATH.resolve()}")

    ensure_output_file_has_markers(OUTPUT_FILE)

    rows = read_csv_rows(CSV_PATH)
    print(f"CSV rows detected (including header): {len(rows)}")

    table_md = csv_to_markdown_table(rows)
    original = OUTPUT_FILE.read_text(encoding="utf-8")
    updated = replace_between_markers(original, START, END, table_md)

    if updated != original:
        OUTPUT_FILE.write_text(updated, encoding="utf-8")
        print("✅ Table written to resources-table.md.")
    else:
        print("ℹ️ No changes written (content identical).")

if __name__ == "__main__":
    sys.exit(main())
