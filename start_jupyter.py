"""
Launch Jupyter with Java kernel available
This script activates the virtual environment and starts Jupyter
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the virtual environment python
    venv_python = Path(__file__).parent / '.venv' / 'Scripts' / 'python.exe'
    
    if not venv_python.exists():
        print("Error: Virtual environment not found!")
        print("Please run: python -m venv .venv")
        print("Then: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if jupyter is installed
    try:
        result = subprocess.run(
            [str(venv_python), '-m', 'jupyter', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Jupyter version: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("Error: Jupyter not installed!")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if Java kernel is installed
    result = subprocess.run(
        [str(venv_python), '-m', 'jupyter', 'kernelspec', 'list'],
        capture_output=True,
        text=True
    )
    
    if 'java' not in result.stdout:
        print("Warning: Java kernel not found!")
        print("Installing Java kernel...")
        subprocess.run(
            [str(venv_python), 'install_kernel.py', '--user'],
            check=True
        )
        print("Java kernel installed successfully!")
    
    print("\n" + "="*60)
    print("Starting Jupyter Notebook with Java kernel...")
    print("="*60)
    print("\nTo create a Java notebook:")
    print("  1. Click 'New' in the Jupyter interface")
    print("  2. Select 'Java' from the kernel list")
    print("  3. Start coding in Java!")
    print("\nOr open the test notebook: test_java.ipynb")
    print("="*60 + "\n")
    
    # Start Jupyter notebook
    try:
        subprocess.run(
            [str(venv_python), '-m', 'jupyter', 'notebook'],
            check=True
        )
    except KeyboardInterrupt:
        print("\nJupyter notebook stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Jupyter: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
