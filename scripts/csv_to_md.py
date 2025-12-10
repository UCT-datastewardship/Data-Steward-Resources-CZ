import csv
from pathlib import Path
import sys

CSV_PATH = Path("data/data.csv")                # <--- change if needed
OUTPUT_FILE = Path("resources-table.md")        # <--- where table goes
START = "<!-- AUTO-TABLE:START -->"
END = "<!-- AUTO-TABLE:END -->"

# --- COLOR MAP (Define outside the function, as before) ---
COLOR_MAP = {
    "Data Steward": "#B3E5FC", # Light Blue
    "Training": "#C8E6C9",     # Light Green
    "Open Science": "#FFF9C4",  # Light Yellow
    "data": "#FFCDD2",         # Light Coral
    "database": "#E1BEE7",     # Light Purple
    "repositories": "#B2EBF2", # Pale Turquoise
    "licensing": "#DCEDC8",    # Mint Green
    "good practices": "#FFE0B2", # Light Peach
    "bad practices": "#F5F5F5",  # Light Gray
    "RDM": "#B2DFDB",          # Soft Teal
    "DMP": "#FFCCBC",          # Soft Orange
    "FAIR": "#F8BBD0",         # Light Pink
    "HE": "#FFFDE7",           # Soft Gold
    "GAČR": "#D7CCC8",         # Light Lavender
    "other": "#D7CCC8",        # Soft Brown
}
# -----------------------------------------------------------

def csv_to_styled_html_table(rows, max_rows=None):
    if not rows:
        return "_No data_"

    if len(rows) < 2:
        # Assuming csv_to_markdown_table is available as a fallback
        return csv_to_markdown_table(rows, max_rows) 

    top_headers = rows[0]
    category_headers = rows[1]
    data_rows = rows[2:]
    
    if max_rows:
        data_rows = data_rows[:max_rows]

    # 1. Store colors for each column
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
        key = h.strip().lower()
        
        # Get color, default to white
        color = COLOR_MAP.get(key, "#FFFFFF") 
        column_colors.append(color) # Save the color for this column
        
        # Apply inline style to the header cell
        style = f' style="background-color: {color};"'
        html_lines.append(f'<th{style}>{h if h else "&nbsp;"}</th>')
    
    html_lines.append("</tr>")
    html_lines.append("</thead>")
    html_lines.append("<tbody>")

    # --- Remaining Data Rows (Styled Data Cells) ---
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
    #end of color map

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

# Updated function to output an HTML table with sticky rows
def csv_to_markdown_table(rows, max_rows=None):
    if not rows:
        return "_No data_"
    headers = rows[0]
    data = rows[1:]
    if max_rows:
        data = data[:max_rows]
        
    # Start with headers
    md = ["|" + "|".join(h if h else " " for h in headers) + "|"]
    
    # Add separator line
    md.append("|" + "|".join("---" for _ in headers) + "|")
    
    # Add data rows
    if data:
        for r in data:
            # Replace internal newlines with space and ensure cell is not empty
            md.append("|" + "|".join((c or " ").replace("\n", " ") for c in r) + "|")
    else:
        # If no data rows, still add an empty row
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
