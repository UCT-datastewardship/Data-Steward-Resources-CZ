import csv
from pathlib import Path
import sys

# --- YOUR ORIGINAL CONSTANTS (FIXED MARKERS) ---
CSV_PATH = Path("data/data.csv")
OUTPUT_FILE = Path("resources-table.md")
# FIX: Restored the actual markers needed by the replace_between_markers function
START = ""
END = ""

# VVVVVV REQUIRED GLOBAL COLOR MAP VVVVVV
COLOR_MAP = {
    # Combined Key for single column in CSV
    "data steward training": "#B3E5FC", # Light Blue (Primary Key for the combined column)
    
    # Rest of the individual keys (added for safety/robustness)
    "data steward": "#B3E5FC",
    "training": "#C8E6C9", 
    "open science": "#FFF9C4",
    "data": "#FFCDD2",
    "database": "#E1BEE7",
    "repositories": "#B2EBF2",
    "licensing": "#DCEDC8",
    "good practices": "#FFE0B2",
    "bad practices": "#F5F5F5",
    "rdm": "#B2DFDB",
    "dmp": "#FFCCBC",
    "fair": "#F8BBD0",
    "he": "#FFFDE7",
    "gačr": "#D7CCC8",
    "other": "#D7CCC8",
}
# ^^^^^^ END COLOR MAP ^^^^^^

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

# VVVVVV REQUIRED FALLBACK FUNCTION (Simple Markdown) VVVVVV
def csv_to_markdown_table(rows, max_rows=None):
    if not rows:
        return "_No data_"
    headers = rows[0]
    data = rows[1:]
    if max_rows:
        data = data[:max_rows]
    
    md = ["|" + "|".join(h if h else " " for h in headers) + "|"]
    md.append("|" + "|".join("---" for _ in headers) + "|")
    
    if data:
        for r in data:
            md.append("|" + "|".join((c or " ").replace("\n", " ") for c in r) + "|")
    else:
        md.append("|" + "|".join(" " for _ in headers) + "|")
        
    return "\n".join(md)
# ^^^^^^ END OF FALLBACK FUNCTION ^^^^^^


# VVVVVV THE NEW STYLED HTML FUNCTION VVVVVV
def csv_to_styled_html_table(rows, max_rows=None):
    if not rows:
        return "_No data_"

    # Assuming a minimum of two rows (Top Header, Categories)
    if len(rows) < 2:
        return csv_to_markdown_table(rows, max_rows)

    top_headers = rows[0]
    category_headers = rows[1]
    data_rows = rows[2:]

    if max_rows:
        data_rows = data_rows[:max_rows]

    # 1. Prepare to store colors for each column
    column_colors = []

    html_lines = ["<table>", "<thead>"]

    # --- ROW 1: Top-Level Header (Unstyled) ---
    html_lines.append("<tr>")
    for h in top_headers:
        html_lines.append(f"<th>{h if h else '&nbsp;'}</th>")
    html_lines.append("</tr>")

    # --- ROW 2: Category Headers (STYLED) and Populate column_colors list ---
    html_lines.append("<tr>")
    for h in category_headers:
        key = h.strip().lower() # Match key case with COLOR_MAP

        # Get color from COLOR_MAP, default to white (#FFFFFF)
        color = COLOR_MAP.get(key, "#FFFFFF")
        column_colors.append(color) # Save the color for the entire column

        # Apply inline style to the header cell
        style = f' style="background-color: {color};"'
        html_lines.append(f'<th{style}>{h if h else "&nbsp;"}</th>')

    html_lines.append("</tr>")
    html_lines.append("</thead>")
    html_lines.append("<tbody>")

    # --- Remaining Data Rows (STYLED Data Cells) ---
    if data_rows:
        for r in data_rows:
            html_lines.append("<tr>")
            for i, cell_content in enumerate(r):
                # Get the color corresponding to the current column index (i)
                color = column_colors[i]

                # Apply inline style to the data cell
                style = f' style="background-color: {color};"'

                content = (cell_content or "&nbsp;").replace("\n", " ")
                # Generate the styled data cell <td>
                html_lines.append(f'<td{style}>{content}</td>')
            html_lines.append("</tr>")

    html_lines.append("</tbody>")
    html_lines.append("</table>")

    return "\n".join(html_lines)
# ^^^^^^ END OF THE NEW STYLED HTML FUNCTION ^^^^^^


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

    # Call the new HTML function
    table_html = csv_to_styled_html_table(rows)
    
    original = OUTPUT_FILE.read_text(encoding="utf-8")
    updated = replace_between_markers(original, START, END, table_html)

    if updated != original:
        OUTPUT_FILE.write_text(updated, encoding="utf-8")
        print("✅ HTML Table written with fully colored columns.")
    else:
        print("ℹ️ No changes written (content identical).")

if __name__ == "__main__":
    sys.exit(main())
