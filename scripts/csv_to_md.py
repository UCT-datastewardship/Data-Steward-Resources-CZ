import csv
from pathlib import Path
import sys

# --- YOUR ORIGINAL CONSTANTS (FIXED MARKERS) ---
CSV_PATH = Path("data/data.csv")
OUTPUT_FILE = Path("resources-table.md")
START = ""  # <-- FIXED
END = ""      # <-- FIXED

# VVVVVV REQUIRED GLOBAL COLOR MAP (FIXED FOR ROBUSTNESS) VVVVVV
COLOR_MAP = {
    # Added "data steward" and made "data steward training" the same color
    "data steward": "#B3E5FC",        # Light Blue (Safety Key)
    "training": "#C8E6C9",            # Light Green (Safety Key)
    
    # Combined Key for single column:
    "data steward training": "#B3E5FC", # Light Blue (Primary Key)
    
    # Rest of the keys...
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

# ... (Rest of your script follows without changes) ...
