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
    "https://github.com/UCT-datastewardship/Data-Steward-Resources-CZ/blob/main/.github/workflows/Resources%20Data%20Stewardship%20-%20git.csv"
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
