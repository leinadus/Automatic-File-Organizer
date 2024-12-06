import tkinter as tk
from tkinter import filedialog
import os


def browse_directory():
    """
    Open a file dialog to select a directory and return its path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Base Directory")
    return directory


def save_directory_path(path, file_path):
    """
    Save the selected directory path to a file.
    """
    with open(file_path, 'w') as f:
        f.write(path)


if __name__ == "__main__":
    base_directory = browse_directory()
    if not base_directory:  # Check if the user cancelled the dialog
        print("No directory selected. Exiting.")
        exit(1)

    # Specify the file where the directory path will be saved
    path_file = 'base_directory.txt'
    save_directory_path(base_directory, path_file)
    print(f"Base directory path saved to {path_file}")
