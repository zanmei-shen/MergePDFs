# Plan: PDF Merger App Development

## TL;DR
Build a Python 3.9+ Tkinter desktop application that merges multiple PDF files into a single PDF with alphabetical sorting and bookmarks. Package as standalone .exe for Windows distribution using PyInstaller.

## Project Structure
MergePDFs/
├── src/
│ ├── init.py
│ ├── main.py # Entry point
│ ├── pdf_merger.py # Core PDF merge logic
│ ├── ui/
│ │ ├── init.py
│ │ └── app.py # Tkinter GUI
│ └── utils/
│ ├── init.py
│ └── file_handler.py # File selection/validation
├── tests/
│ ├── init.py
│ └── test_pdf_merger.py # Unit tests

## Dependencies
- **pypdf** (or PyPDF2): PDF manipulation
- **Tkinter**: Built-in with Python
- **PyInstaller**: For .exe generation (dev-only)

## Steps

### Phase 1: Core Logic (Non-UI)
1. Create `pdf_merger.py` with class `PDFMerger` that:
   - Takes a list of PDF file paths
   - Sorts them alphabetically
   - Merges them into one PDF
   - Adds bookmarks for each source file
   - Saves to output path
   - Handles errors (missing files, corrupted PDFs)

2. Create `file_handler.py` utilities for:
   - Validating PDF files
   - Sorting by filename
   - Batch reading from folder

### Phase 2: UI Development
3. Create `ui/app.py` Tkinter interface with:
   - **File selection**: Browse & add individual PDFs (button → file dialog)
   - **Folder selection**: Add entire folder of PDFs (button → folder dialog)
   - **File list**: Display selected PDFs with remove/reorder buttons
   - **Output path**: Input field for where to save merged PDF
   - **Auto-sort toggle**: Checkbox to enable/disable alphabetical sorting
   - **Merge button**: Trigger merge with progress indicator
   - **Status bar**: Display messages (success/errors)

4. Connect UI to `PDFMerger` class

### Phase 3: Testing & Validation
5. Write unit tests in `tests/test_pdf_merger.py`:
   - Test PDF merging with sample PDFs
   - Test bookmark generation
   - Test alphabetical sorting
   - Test error handling (corrupted files, invalid paths)

6. Manual testing:
   - Merge 2-3 test PDFs
   - Verify bookmark structure in output
   - Verify sort order
   - Test edge cases (empty folder, single file, special characters in names)

### Phase 4: Packaging
7. Create `requirements.txt` with pypdf, PyInstaller

8. Create `.gitignore` for Python projects (venv/, __pycache__/, *.exe, dist/, build/)

9. Build standalone .exe:
   - Create `.spec` file for PyInstaller configuration
   - Use `pyinstaller merge_pdf_app.spec` to generate .exe
   - Test .exe on clean Windows machine

## Relevant Files to Create
- `src/pdf_merger.py` — Core merge logic: `PDFMerger` class with methods `merge()`, `add_bookmarks()`, `sort_files()`
- `src/ui/app.py` — Tkinter GUI: `PDFMergerApp` class with widgets for file selection, output path, merge button
- `src/utils/file_handler.py` — Utilities: `validate_pdf()`, `sort_by_filename()`, `get_pdfs_from_folder()`
- `src/main.py` — Entry point: Initialize and run `PDFMergerApp`
- `requirements.txt` — List: pypdf, PyInstaller (dev)
- `tests/test_pdf_merger.py` — Unit tests using unittest or pytest
- `.gitignore` — Standard Python gitignore

## Verification
1. **Unit tests pass**: Run `python -m pytest tests/` — all tests green
2. **Merge functionality**: Create 3 test PDFs (A.pdf, C.pdf, B.pdf), merge them, verify output has bookmarks and correct order
3. **UI responsiveness**: Click buttons, verify file dialogs work, verify status messages appear
4. **Error handling**: Try merging corrupted PDF, verify graceful error message
5. **Standalone .exe**: Generate .exe, run on another Windows machine without Python installed, verify it works
6. **Edge cases**:
   - Merge single PDF (should work)
   - Merge empty folder selection (should error gracefully)
   - Filenames with special characters (Chinese, spaces, etc.)

## Decisions
- **PDF library**: pypdf chosen (actively maintained, more modern than PyPDF2)
- **Scope**: Full features as specified (bookmarks, sorting, batch folder import)
- **UI**: Tkinter for simplicity and cross-platform support
- **Packaging**: PyInstaller for standalone .exe (no Python installation required for end users)
- **Testing**: Unit tests for core logic; manual testing for UI due to Tkinter complexity

## Further Considerations
1. **Error recovery**: Should the app validate files before merge starts or fail mid-merge? → Validate upfront, show which files are invalid before merge begins
2. **Bookmark naming**: Use source filename or generic "Page N"? → Use source filename for clarity
3. **UI enhancements later**: Drag-and-drop for file adding, PDF preview, batch processing → Out of scope for MVP, can add later