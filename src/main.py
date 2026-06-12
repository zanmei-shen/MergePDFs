"""Main entry point for PDF Merger App"""

import sys
import os

# Add parent directory to path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app import main

if __name__ == "__main__":
    main()
