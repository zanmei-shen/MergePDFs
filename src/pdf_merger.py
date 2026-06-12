"""Core PDF merging logic for PDF Merger App"""

import os
from pathlib import Path
from typing import List, Optional
from pypdf import PdfWriter, PdfReader


class PDFMerger:
    """Handles PDF merging with sorting and bookmarks."""
    
    def __init__(self):
        """Initialize the PDF merger."""
        self.merger = None
        self.files_to_merge = []
    
    def sort_files(self, file_paths: List[str]) -> List[str]:
        """
        Sort PDF file paths alphabetically by filename.
        
        Args:
            file_paths: List of absolute paths to PDF files
            
        Returns:
            Sorted list of file paths
        """
        return sorted(file_paths, key=lambda x: os.path.basename(x).lower())
    
    def validate_pdf(self, file_path: str) -> bool:
        """
        Validate that a file is a readable PDF.
        
        Args:
            file_path: Path to potential PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        if not os.path.exists(file_path):
            return False
        
        if not file_path.lower().endswith('.pdf'):
            return False
        
        try:
            with open(file_path, 'rb') as f:
                PdfReader(f)
            return True
        except Exception:
            return False
    
    def merge(
        self,
        input_files: List[str],
        output_path: str,
        sort_alphabetically: bool = True,
        add_bookmarks: bool = True
    ) -> tuple[bool, str]:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            input_files: List of paths to PDF files to merge
            output_path: Path where merged PDF should be saved
            sort_alphabetically: Whether to sort files before merging
            add_bookmarks: Whether to add bookmarks for each file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate all input files
            invalid_files = [f for f in input_files if not self.validate_pdf(f)]
            if invalid_files:
                return False, f"Invalid PDF files: {', '.join([os.path.basename(f) for f in invalid_files])}"
            
            if not input_files:
                return False, "No PDF files to merge."
            
            # Sort files if requested
            files_to_merge = self.sort_files(input_files) if sort_alphabetically else input_files
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Merge PDFs
            if add_bookmarks:
                self._merge_with_bookmarks(files_to_merge, output_path)
            else:
                self._merge_without_bookmarks(files_to_merge, output_path)
            
            return True, f"Successfully merged {len(files_to_merge)} PDFs to {os.path.basename(output_path)}"
        
        except Exception as e:
            return False, f"Error during merge: {str(e)}"
    
    def _merge_without_bookmarks(self, input_files: List[str], output_path: str) -> None:
        """
        Merge PDFs without bookmarks using PdfWriter.
        
        Args:
            input_files: List of PDF file paths
            output_path: Output file path
        """
        writer = PdfWriter()
        
        for pdf_file in input_files:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    def _merge_with_bookmarks(self, input_files: List[str], output_path: str) -> None:
        """
        Merge PDFs and add bookmarks for each source file.
        
        Args:
            input_files: List of PDF file paths
            output_path: Output file path
        """
        writer = PdfWriter()
        current_page = 0
        
        for pdf_file in input_files:
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)
            
            # Add all pages from this PDF
            for page in reader.pages:
                writer.add_page(page)
            
            # Add outline/bookmark for this file at the start page
            bookmark_title = Path(pdf_file).stem  # Filename without extension
            writer.add_outline_item(bookmark_title, current_page)
            
            current_page += num_pages
        
        # Write output
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
