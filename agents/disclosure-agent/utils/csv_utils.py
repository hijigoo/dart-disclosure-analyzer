"""
CSV Utility Module

This module provides functions for exporting disclosure data to CSV files
and for reading and processing CSV data with filtering capabilities.
"""

import os
import csv
import json
from datetime import datetime
from pathlib import Path

def ensure_download_directory():
    """
    Ensure that the data directory exists

    Returns:
        Path: Path to the data directory
    """
    # Create path to data directory at the root of the project
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = project_root / 'download'

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
    data_dir = ensure_download_directory()

    # Generate a default filename if not provided
    if not filename:
        # current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_time = datetime.now().strftime("%Y%m%d")
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

        # print(f"Successfully saved {len(disclosures)} disclosures to {file_path}")
        return str(file_path)

    except Exception as e:
        print(f"Error saving disclosures to CSV: {str(e)}")
        return None


def read_csv_filter_to_json(file_path, column_name, keyword):
    """
    Read a CSV file and filter rows where the specified column contains the keyword.
    Convert the filtered rows to JSON format.

    Args:
        file_path: Path to the CSV file (absolute or relative to current working directory)
        column_name: Name of the column to search in
        keyword: Keyword to search for in the specified column

    Returns:
        dict: JSON-serializable dictionary with filtered rows
        {
            "filtered_rows": [row1, row2, ...],
            "total_rows": total number of rows in the CSV,
            "matched_rows": number of rows that matched the filter
        }
    """
    try:
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Check if file exists
        if not file_path.exists():
            print(f"Error: File not found at {file_path}")
            return None

        filtered_rows = []
        total_rows = 0

        # Read CSV file
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Check if specified column exists
            if column_name not in reader.fieldnames:
                print(f"Error: Column '{column_name}' not found in CSV. Available columns: {reader.fieldnames}")
                return None

            # Process rows
            for row in reader:
                total_rows += 1
                # Check if keyword is in the specified column
                if keyword.lower() in row[column_name].lower():
                    filtered_rows.append(row)

        # Prepare result dictionary
        result = {
            "filtered_rows": filtered_rows,
            "total_rows": total_rows,
            "matched_rows": len(filtered_rows)
        }

        # print(f"Found {len(filtered_rows)} matching rows out of {total_rows} total rows")
        return result

    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None


def read_csv_filter_to_json_string(file_path, column_name, keyword, indent=2):
    """
    Read a CSV file, filter rows where the specified column contains the keyword,
    and return the result as a JSON string.

    Args:
        file_path: Path to the CSV file
        column_name: Name of the column to search in
        keyword: Keyword to search for in the specified column
        indent: Number of spaces for JSON indentation (default: 2)

    Returns:
        str: JSON string with filtered rows, or None if an error occurred
    """
    result = read_csv_filter_to_json(file_path, column_name, keyword)

    if result:
        try:
            return json.dumps(result, indent=indent, ensure_ascii=False)
        except Exception as e:
            print(f"Error converting to JSON string: {str(e)}")
            return None

    return None


def get_latest_by_rcept_dt(data: dict) -> dict:
    """
    JSON 데이터를 받아서 rcept_dt가 가장 최근인 항목을 반환하는 함수

    Args:
        data (dict): {'filtered_rows': [...], 'total_rows': int, 'matched_rows': int}

    Returns:
        dict: 가장 최근 rcept_dt를 가진 JSON 항목
    """
    if "filtered_rows" not in data or not data["filtered_rows"]:
        return {}

    # rcept_dt를 기준으로 가장 최근 항목 선택
    latest = max(data["filtered_rows"], key=lambda x: x["rcept_dt"])
    return latest
