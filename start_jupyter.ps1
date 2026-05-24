# PowerShell script to start Jupyter with Java kernel
# Run this with: .\start_jupyter.ps1

Write-Host "Starting Java Kernel for Jupyter..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Then run: .venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment and start Jupyter
& .venv\Scripts\python.exe start_jupyter.py
