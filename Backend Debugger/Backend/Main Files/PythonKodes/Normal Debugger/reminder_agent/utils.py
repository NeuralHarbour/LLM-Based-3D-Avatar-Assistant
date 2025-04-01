# utils.py
import os

def ensure_file_exists(file_path):
    """Ensure the file exists, creating it if necessary."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")
        print(f"Created file: {file_path}")