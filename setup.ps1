# VoxPolish Setup Script for Windows
# Initialize environment and install dependencies

Write-Host "--- VoxPolish Setup ---" -ForegroundColor Cyan

# Check for venv
if (!(Test-Path venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate and install
Write-Host "Installing dependencies from requirements.txt..."
.\venv\Scripts\pip install -r requirements.txt

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To start development, activate the environment:"
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
