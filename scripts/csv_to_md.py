import csv
from pathlib import Path
import sys

CSV_PATH = Path("data/data.csv")                # <--- change if needed
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

# Updated function to output an HTML table with sticky rows
def csv_to_html_table(rows, max_rows=None):
    if not rows:
        return "_No data_"

    headers = rows[0]
    data_rows = rows[1:]

    # 1. Define the custom CSS for sticky headers
    # Note: These values (30px, 60px) are based on standard row heights. 
    # Adjust 'top' values if your rows are significantly taller or shorter.
    css = """
<style>
  /* Base style for all sticky cells */
  .sticky-header-cell {
    position: sticky;
    background-color: #f7f7f7; /* Light gray background to hide content below */
    z-index: 2; /* Ensures it stays on top of the scrolling content */
  }
  /* Sticky Row 1 (Header row) sticks to the very top (top: 0) */
  .sticky-row-1 {
    top: 0;
    border-bottom: 1px solid #ccc;
  }
  /* Sticky Row 2 sticks below Sticky Row 1. If Row 1 is 30px tall, Row 2 sticks at 30px */
  .sticky-row-2 {
    top: 30px; 
    border-bottom: 1px solid #ccc;
  }
</style>
"""
    
    # 2. Start HTML Table structure
    html_lines = [css, "<table>", "<thead>"]

    # --- ROW 1 (The original header row) ---
    html_lines.append("<tr>")
    for h in headers:
        # Apply sticky classes for the first row
        cell_content = h if h else '&nbsp;'
        html_lines.append(f'<th class="sticky-header-cell sticky-row-1">{cell_content}</th>')
    html_lines.append("</tr>")

    # --- ROW 2 (The first data row, which you want to freeze) ---
    if data_rows:
        second_row_data = data_rows[0] # Get the data for the second row
        data_rows = data_rows[1:]      # Remove the first data row from the main data list

        html_lines.append("<tr>")
        for cell_content in second_row_data:
            # Apply sticky classes for the second row
            content = (cell_content or "&nbsp;").replace("\n", " ")
            html_lines.append(f'<td class="sticky-header-cell sticky-row-2">{content}</td>')
        html_lines.append("</tr>")
    
    html_lines.append("</thead>")
    html_lines.append("<tbody>")

    # --- Remaining Data Rows (Normal scrolling content) ---
    if data_rows:
        for r in data_rows:
            html_lines.append("<tr>")
            for cell_content in r:
                content = (cell_content or "&nbsp;").replace("\n", " ")
                html_lines.append(f"<td>{content}</td>")
            html_lines.append("</tr>")
    
    html_lines.append("</tbody>")
    html_lines.append("</table>")

    return "\n".join(html_lines)


# Update the main function to call the new HTML function
def main():
    print(f"Output file: {OUTPUT_FILE.resolve()}")
    print(f"CSV path:    {CSV_PATH.resolve()}")

    ensure_output_file_has_markers(OUTPUT_FILE)

    rows = read_csv_rows(CSV_PATH)
    print(f"CSV rows detected (including header): {len(rows)}")

    # !!! Ensure you call the HTML function here !!!
    table_html = csv_to_html_table(rows) 
    
    original = OUTPUT_FILE.read_text(encoding="utf-8")
    updated = replace_between_markers(original, START, END, table_html)

    if updated != original:
        OUTPUT_FILE.write_text(updated, encoding="utf-8")
        print("✅ HTML Table written with attempted sticky headers.")
    else:
        print("ℹ️ No changes written (content identical).")

# ... (The rest of your script remains the same) ...

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
