"""Unit tests for PDF Merger App"""

import unittest
import os
import tempfile
from pathlib import Path
from pypdf import PdfWriter

from src.pdf_merger import PDFMerger
from src.utils.file_handler import (
    validate_pdf,
    get_pdfs_from_folder,
    sort_by_filename,
    get_default_output_path
)


class TestPDFMerger(unittest.TestCase):
    """Test cases for PDFMerger class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.merger = PDFMerger()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_pdf(self, filename: str) -> str:
        """
        Create a simple test PDF file.
        
        Args:
            filename: Name of the PDF file to create
            
        Returns:
            Full path to created PDF
        """
        file_path = os.path.join(self.temp_dir, filename)
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        with open(file_path, 'wb') as f:
            writer.write(f)
        return file_path
    
    def test_validate_pdf_valid(self):
        """Test validation of valid PDF file."""
        pdf_path = self._create_test_pdf("test.pdf")
        self.assertTrue(self.merger.validate_pdf(pdf_path))
    
    def test_validate_pdf_invalid_extension(self):
        """Test validation fails for non-PDF files."""
        txt_path = os.path.join(self.temp_dir, "test.txt")
        with open(txt_path, 'w') as f:
            f.write("test")
        self.assertFalse(self.merger.validate_pdf(txt_path))
    
    def test_validate_pdf_nonexistent(self):
        """Test validation fails for nonexistent files."""
        self.assertFalse(self.merger.validate_pdf("/nonexistent/path.pdf"))
    
    def test_sort_files_alphabetically(self):
        """Test that files are sorted alphabetically."""
        files = [
            "/path/to/c_file.pdf",
            "/path/to/a_file.pdf",
            "/path/to/b_file.pdf"
        ]
        sorted_files = self.merger.sort_files(files)
        expected = [
            "/path/to/a_file.pdf",
            "/path/to/b_file.pdf",
            "/path/to/c_file.pdf"
        ]
        self.assertEqual(sorted_files, expected)
    
    def test_merge_single_pdf(self):
        """Test merging a single PDF."""
        pdf1 = self._create_test_pdf("single.pdf")
        output = os.path.join(self.temp_dir, "output.pdf")
        
        success, message = self.merger.merge([pdf1], output)
        
        print(f"Merge result: success={success}, message={message}")
        self.assertTrue(success, f"Merge failed: {message}")
    
    def test_merge_multiple_pdfs(self):
        """Test merging multiple PDFs."""
        pdf1 = self._create_test_pdf("a.pdf")
        pdf2 = self._create_test_pdf("b.pdf")
        pdf3 = self._create_test_pdf("c.pdf")
        output = os.path.join(self.temp_dir, "merged.pdf")
        
        success, message = self.merger.merge([pdf1, pdf2, pdf3], output)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output))
    
    def test_merge_empty_list(self):
        """Test that merge with empty list fails gracefully."""
        output = os.path.join(self.temp_dir, "output.pdf")
        success, message = self.merger.merge([], output)
        
        self.assertFalse(success)
        self.assertIn("No PDF files", message)
    
    def test_merge_invalid_file(self):
        """Test that merge with invalid file fails gracefully."""
        pdf1 = self._create_test_pdf("valid.pdf")
        invalid_path = "/nonexistent/invalid.pdf"
        output = os.path.join(self.temp_dir, "output.pdf")
        
        success, message = self.merger.merge([pdf1, invalid_path], output)
        
        self.assertFalse(success)
        self.assertIn("Invalid PDF", message)
    
    def test_merge_with_sorting(self):
        """Test that merge respects sort option."""
        pdf1 = self._create_test_pdf("c.pdf")
        pdf2 = self._create_test_pdf("a.pdf")
        pdf3 = self._create_test_pdf("b.pdf")
        output = os.path.join(self.temp_dir, "merged.pdf")
        
        success, message = self.merger.merge(
            [pdf1, pdf2, pdf3],
            output,
            sort_alphabetically=True
        )
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output))


class TestFileHandler(unittest.TestCase):
    """Test cases for file_handler utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_pdf(self, filename: str) -> str:
        """Create a test PDF."""
        file_path = os.path.join(self.temp_dir, filename)
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        with open(file_path, 'wb') as f:
            writer.write(f)
        return file_path
    
    def test_validate_pdf_valid(self):
        """Test PDF validation with valid file."""
        pdf_path = self._create_test_pdf("test.pdf")
        self.assertTrue(validate_pdf(pdf_path))
    
    def test_validate_pdf_invalid(self):
        """Test PDF validation with invalid file."""
        txt_path = os.path.join(self.temp_dir, "test.txt")
        with open(txt_path, 'w') as f:
            f.write("test")
        self.assertFalse(validate_pdf(txt_path))
    
    def test_get_pdfs_from_folder(self):
        """Test getting PDFs from a folder."""
        self._create_test_pdf("a.pdf")
        self._create_test_pdf("b.pdf")
        # Also create a non-PDF file
        with open(os.path.join(self.temp_dir, "readme.txt"), 'w') as f:
            f.write("test")
        
        pdfs = get_pdfs_from_folder(self.temp_dir)
        
        self.assertEqual(len(pdfs), 2)
        self.assertTrue(all(f.endswith('.pdf') for f in pdfs))
    
    def test_get_pdfs_from_nonexistent_folder(self):
        """Test that nonexistent folder raises error."""
        with self.assertRaises(ValueError):
            get_pdfs_from_folder("/nonexistent/folder")
    
    def test_sort_by_filename(self):
        """Test sorting files by filename."""
        files = [
            "/path/to/c.pdf",
            "/path/to/a.pdf",
            "/path/to/b.pdf"
        ]
        sorted_files = sort_by_filename(files)
        expected = [
            "/path/to/a.pdf",
            "/path/to/b.pdf",
            "/path/to/c.pdf"
        ]
        self.assertEqual(sorted_files, expected)
    
    def test_get_default_output_path(self):
        """Test default output path generation."""
        input_files = ["/path/to/file1.pdf", "/path/to/file2.pdf"]
        output = get_default_output_path(input_files)
        
        self.assertIn("merged_output.pdf", output)
        self.assertTrue(output.endswith("merged_output.pdf"))
    
    def test_get_default_output_path_empty(self):
        """Test default output path for empty input."""
        output = get_default_output_path([])
        
        self.assertIn("merged_pdfs.pdf", output)


if __name__ == "__main__":
    unittest.main()
