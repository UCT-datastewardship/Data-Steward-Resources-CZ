# sync_sheet.py
import os
import sys
import io
import requests
import pandas as pd

# Either put the full CSV export URL in SHEET_CSV_URL
# or just set YOUR_SHEET_ID below.
SHEET_CSV_URL = os.getenv(
    "SHEET_CSV_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQDeitSl4vNEHlpzWkFBI_NEdskybm7UVtNpK9NVYNzB66V6XuH435QLcu0mAX2fwzLP3OKQCgjux6h/pub?gid=621672034&single=true&output=csv"
)

OUTPUT_CSV = os.getenv("OUTPUT_CSV", "data.csv")
OUTPUT_MD  = os.getenv("OUTPUT_MD",  "TABLE.md")

def main():
    try:
        r = requests.get(SHEET_CSV_URL, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to download sheet CSV: {e}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(io.StringIO(r.text))
    df.to_csv(OUTPUT_CSV, index=False)

    # Markdown export (requires 'tabulate', which the workflow installs)
    try:
        import tabulate  # noqa: F401
        md = df.to_markdown(index=False)
        with open(OUTPUT_MD, "w", encoding="utf-8") as f:
            f.write(md + "\n")
        print(f"Wrote {OUTPUT_CSV} and {OUTPUT_MD}")
    except Exception as e:
        print(f"Wrote {OUTPUT_CSV}. Skipped Markdown export: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
