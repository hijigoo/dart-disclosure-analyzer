"""
CSV Utility Module

This module provides functions for exporting disclosure data to CSV files.
"""

import os
import csv
from datetime import datetime
from pathlib import Path

def ensure_data_directory():
    """
    Ensure that the data directory exists

    Returns:
        Path: Path to the data directory
    """
    # Create path to data directory at the root of the project
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = project_root / 'data'

    # Create directory if it doesn't exist
    if not data_dir.exists():
        data_dir.mkdir()
        print(f"Created data directory at {data_dir}")

    return data_dir

def save_disclosures_to_csv(disclosures, filename=None):
    """
    Save disclosure list to a CSV file in the data directory

    Args:
        disclosures: List of disclosure documents
        filename: Optional filename (without path or extension)

    Returns:
        str: Path to the saved CSV file
    """
    if not disclosures:
        print("No disclosures to save.")
        return None

    # Ensure the data directory exists
    data_dir = ensure_data_directory()

    # Generate a default filename if not provided
    if not filename:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"disclosures_{current_time}"

    # Create the full file path
    file_path = data_dir / f"{filename}.csv"

    try:
        # Determine CSV field names based on first disclosure's keys
        fieldnames = list(disclosures[0].keys())

        # Write disclosures to CSV file
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for disclosure in disclosures:
                writer.writerow(disclosure)

        print(f"Successfully saved {len(disclosures)} disclosures to {file_path}")
        return str(file_path)

    except Exception as e:
        print(f"Error saving disclosures to CSV: {str(e)}")
        return None