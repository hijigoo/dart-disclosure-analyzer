
import os
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