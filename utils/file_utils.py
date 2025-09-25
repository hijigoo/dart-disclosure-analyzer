"""
File Utility Module

This module provides utility functions for file operations,
such as extracting ZIP files and handling file paths.
"""

import os
import shutil
import zipfile
from pathlib import Path


def extract_zip_file(zip_path, extract_path=None, delete_zip=False):
    """
    Extract contents from a ZIP file to a specified directory.

    Args:
        zip_path (str or Path): Path to the ZIP file to extract
        extract_path (str or Path, optional): Directory to extract files to.
            If None, extracts to a directory with the same name as the ZIP file
        delete_zip (bool, optional): Whether to delete the ZIP file after extraction

    Returns:
        str: Path to the directory containing extracted files or None if extraction failed
    """
    try:
        # Convert string paths to Path objects
        zip_path = Path(zip_path)

        # Check if the ZIP file exists
        if not zip_path.exists():
            print(f"Error: ZIP file not found at {zip_path}")
            return None

        # If no extraction path is provided, create one based on the ZIP filename
        if not extract_path:
            # Use the ZIP filename without extension as the extraction directory
            extract_path = zip_path.parent / zip_path.stem
        else:
            extract_path = Path(extract_path)

        # Create extraction directory if it doesn't exist
        extract_path.mkdir(parents=True, exist_ok=True)

        # Extract all files from the ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files in the ZIP
            file_list = zip_ref.namelist()

            # Extract all files
            # print(f"Extracting {len(file_list)} files from {zip_path}...")
            zip_ref.extractall(path=extract_path)
            # print(f"Files extracted to {extract_path}")

        # Delete ZIP file if requested
        if delete_zip:
            os.remove(zip_path)
            # print(f"Deleted original ZIP file: {zip_path}")

        return str(extract_path)

    except zipfile.BadZipFile:
        print(f"Error: The file is not a valid ZIP file: {zip_path}")
        return None
    except PermissionError:
        print(f"Error: Permission denied while extracting {zip_path}")
        return None
    except Exception as e:
        print(f"Error extracting ZIP file: {str(e)}")
        return None


def list_extracted_files(extract_path, extensions=None):
    """
    List all files in the extraction directory, optionally filtered by extensions.

    Args:
        extract_path (str or Path): Directory containing extracted files
        extensions (list, optional): List of file extensions to filter by (e.g., ['.xml', '.html'])

    Returns:
        list: List of file paths matching the criteria
    """
    try:
        extract_path = Path(extract_path)

        if not extract_path.exists() or not extract_path.is_dir():
            print(f"Error: Directory not found or not a directory: {extract_path}")
            return []

        # Get all files in the directory and its subdirectories
        all_files = []
        for root, _, files in os.walk(extract_path):
            for file in files:
                file_path = Path(root) / file
                # If extensions filter is provided, only include matching files
                if extensions:
                    if any(file.lower().endswith(ext.lower()) for ext in extensions):
                        all_files.append(str(file_path))
                else:
                    all_files.append(str(file_path))

        return all_files

    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return []