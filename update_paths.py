#!/usr/bin/env python3
"""
Script to update hardcoded project paths in Python files
"""

import os
import sys
import re

NEW_PROJECT_NAME = "dart-disclosure-viewer"
OLD_PROJECT_PATH = "/Users/kichul/Documents/project/dart-disclosure-viewer"
NEW_PROJECT_PATH = f"/Users/kichul/Documents/project/{NEW_PROJECT_NAME}"

def update_file(file_path):
    """Update paths in a single file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace hardcoded paths
    updated_content = content.replace(OLD_PROJECT_PATH, NEW_PROJECT_PATH)
    
    # Check if any changes were made
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        return True
    
    return False

def scan_directory(directory):
    """Recursively scan directory for Python files and update paths"""
    updated_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if update_file(file_path):
                    updated_files.append(file_path)
    
    return updated_files

def update_readme():
    """Update project name in README.md"""
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the title (assumes it's the first heading)
        updated_content = re.sub(r'^# .+', f'# DART 공시정보 조회 프로그램', content, count=1)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    
    return False

def main():
    print(f"Updating paths from '{OLD_PROJECT_PATH}' to '{NEW_PROJECT_PATH}'...")
    
    # Update Python files
    python_files = scan_directory('.')
    print(f"Updated {len(python_files)} Python files:")
    for file in python_files:
        print(f"  - {file}")
    
    # Update README
    if update_readme():
        print("Updated README.md with new project name")
    
    print("\nDone! To complete the renaming process:")
    print(f"1. Create a new directory: mkdir -p {NEW_PROJECT_PATH}")
    print(f"2. Copy files: cp -r api display utils download *.py .gitignore README.md {NEW_PROJECT_PATH}/")
    print(f"3. Test your project in the new location")

if __name__ == "__main__":
    main()