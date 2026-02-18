# Quick start script for the sensor backend server (Windows PowerShell)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Sensor Backend Server - Quick Start" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Python is not installed" -ForegroundColor Red
    exit 1
}

# Check if pip is installed
try {
    $null = pip --version 2>&1
    Write-Host "✓ pip found" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: pip is not installed" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created (using default settings)" -ForegroundColor Green
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Ask about Docker Compose
Write-Host ""
Write-Host "Do you want to start Mosquitto MQTT broker with Docker? (y/n)" -ForegroundColor Cyan
$response = Read-Host

if ($response -eq "y" -or $response -eq "Y") {
    try {
        $null = docker-compose --version 2>&1
        Write-Host ""
        Write-Host "Starting Mosquitto broker..." -ForegroundColor Yellow
        docker-compose up -d
        Write-Host "✓ Mosquitto started on tcp://localhost:1883" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "Docker Compose not found. Please start your MQTT broker manually." -ForegroundColor Yellow
    }
}

# Start the server
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Starting Sensor Backend Server..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python main.py
