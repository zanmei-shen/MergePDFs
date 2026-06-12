"""Tkinter GUI for PDF Merger App"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from typing import List

from src.pdf_merger import PDFMerger
from src.utils.file_handler import get_pdfs_from_folder, get_default_output_path


class PDFMergerApp:
    """Main Tkinter application for PDF merging."""
    
    def __init__(self, root):
        """
        Initialize the PDF Merger GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        self.merger = PDFMerger()
        self.file_list = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Title
        title_label = tk.Label(
            self.root,
            text="PDF Merger",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.root, text="Select PDF Files", padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Button frame for file operations
        button_frame = tk.Frame(file_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        add_file_btn = ttk.Button(
            button_frame,
            text="Add File(s)",
            command=self._add_files
        )
        add_file_btn.pack(side=tk.LEFT, padx=5)
        
        add_folder_btn = ttk.Button(
            button_frame,
            text="Add Folder",
            command=self._add_folder
        )
        add_folder_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = ttk.Button(
            button_frame,
            text="Remove Selected",
            command=self._remove_file
        )
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear All",
            command=self._clear_list
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # File list with scrollbar
        list_frame = tk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Options frame
        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Sort checkbox
        self.sort_var = tk.BooleanVar(value=True)
        sort_check = ttk.Checkbutton(
            options_frame,
            text="Sort files alphabetically",
            variable=self.sort_var
        )
        sort_check.pack(anchor=tk.W)
        
        # Bookmarks checkbox
        self.bookmarks_var = tk.BooleanVar(value=True)
        bookmarks_check = ttk.Checkbutton(
            options_frame,
            text="Add bookmarks for each file",
            variable=self.bookmarks_var
        )
        bookmarks_check.pack(anchor=tk.W)
        
        # Output frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(output_frame, text="Output File:").pack(anchor=tk.W)
        
        output_path_frame = tk.Frame(output_frame)
        output_path_frame.pack(fill=tk.X, pady=5)
        
        self.output_path_var = tk.StringVar(value="merged_output.pdf")
        output_entry = ttk.Entry(
            output_path_frame,
            textvariable=self.output_path_var,
            width=50
        )
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(
            output_path_frame,
            text="Browse",
            command=self._browse_output
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            fg="green",
            justify=tk.LEFT,
            wraplength=680
        )
        self.status_label.pack(anchor=tk.W)
        
        # Merge button (prominent)
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=15)
        
        merge_btn = ttk.Button(
            button_frame,
            text="▶ MERGE PDFs",
            command=self._merge_pdfs
        )
        merge_btn.pack(fill=tk.X, ipady=10)
    
    def _add_files(self):
        """Open file dialog to select PDF files."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
        self._update_listbox()
    
    def _add_folder(self):
        """Open folder dialog to select a folder of PDFs."""
        folder = filedialog.askdirectory(title="Select folder with PDFs")
        if folder:
            try:
                pdfs = get_pdfs_from_folder(folder)
                if not pdfs:
                    messagebox.showwarning(
                        "No PDFs",
                        f"No PDF files found in {folder}"
                    )
                    return
                
                for pdf in pdfs:
                    if pdf not in self.file_list:
                        self.file_list.append(pdf)
                self._update_listbox()
                self._set_status(f"Added {len(pdfs)} PDFs from folder", "green")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def _remove_file(self):
        """Remove selected file from list."""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            del self.file_list[index]
            self._update_listbox()
    
    def _clear_list(self):
        """Clear all files from list."""
        if messagebox.askyesno("Clear", "Remove all files from list?"):
            self.file_list.clear()
            self._update_listbox()
    
    def _browse_output(self):
        """Open file dialog to select output file path."""
        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile="merged_output.pdf"
        )
        if file:
            self.output_path_var.set(file)
    
    def _update_listbox(self):
        """Update the file list display."""
        self.file_listbox.delete(0, tk.END)
        for file in self.file_list:
            self.file_listbox.insert(tk.END, os.path.basename(file))
        self._set_status(f"{len(self.file_list)} file(s) selected", "blue")
    
    def _set_status(self, message: str, color: str = "black"):
        """
        Update status label.
        
        Args:
            message: Status message text
            color: Text color
        """
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def _merge_pdfs(self):
        """Merge the selected PDFs."""
        if not self.file_list:
            messagebox.showwarning("No Files", "Please select at least one PDF file.")
            return
        
        output_path = self.output_path_var.get()
        if not output_path:
            messagebox.showwarning("No Output", "Please specify an output file path.")
            return
        
        self._set_status("Merging PDFs...", "blue")
        
        success, message = self.merger.merge(
            input_files=self.file_list,
            output_path=output_path,
            sort_alphabetically=self.sort_var.get(),
            add_bookmarks=self.bookmarks_var.get()
        )
        
        if success:
            self._set_status(message, "green")
            messagebox.showinfo("Success", message)
        else:
            self._set_status(message, "red")
            messagebox.showerror("Merge Failed", message)


def main():
    """Launch the PDF Merger application."""
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
