"""File handling utilities for PDF Merger App"""

import os
from pathlib import Path
from typing import List


def validate_pdf(file_path: str) -> bool:
    """
    Validate that a file is a PDF.
    
    Args:
        file_path: Path to potential PDF file
        
    Returns:
        True if file exists and has .pdf extension, False otherwise
    """
    if not os.path.exists(file_path):
        return False
    return file_path.lower().endswith('.pdf')


def get_pdfs_from_folder(folder_path: str) -> List[str]:
    """
    Get all PDF files from a folder (non-recursive).
    
    Args:
        folder_path: Path to folder
        
    Returns:
        List of absolute paths to PDF files found
        
    Raises:
        ValueError: If folder doesn't exist
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"Folder does not exist: {folder_path}")
    
    pdf_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and validate_pdf(file_path):
            pdf_files.append(file_path)
    
    return pdf_files


def sort_by_filename(file_paths: List[str]) -> List[str]:
    """
    Sort file paths alphabetically by filename.
    
    Args:
        file_paths: List of file paths
        
    Returns:
        Sorted list of file paths
    """
    return sorted(file_paths, key=lambda x: os.path.basename(x).lower())


def get_default_output_path(input_files: List[str]) -> str:
    """
    Generate a default output path based on input files.
    
    Args:
        input_files: List of input PDF paths
        
    Returns:
        Suggested output path (same directory as first file)
    """
    if not input_files:
        return os.path.expanduser("~/merged_pdfs.pdf")
    
    first_file_dir = os.path.dirname(input_files[0])
    return os.path.join(first_file_dir, "merged_output.pdf")
