#!/usr/bin/env powershell

# Quick start script for the sensor backend server (Windows PowerShell)

Write-Host '========================================='
Write-Host 'Sensor Backend Server - Quick Start'
Write-Host '========================================='

# Check if Python is installed
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = (& python --version) 2>&1
    Write-Host ('Python found: ' + $pythonVersion)
} else {
    Write-Host 'Error: Python is not installed'
    exit 1
}

# Check if pip is installed
$pipCmd = Get-Command pip -ErrorAction SilentlyContinue
if ($pipCmd) {
    $pipVersion = (& pip --version) 2>&1
    Write-Host ('pip found: ' + $pipVersion)
} else {
    Write-Host 'Error: pip is not installed'
    exit 1
}

# Create .env file if it does not exist
if (-not (Test-Path '.env')) {
    Write-Host ''
    Write-Host 'Creating .env file from template...'
    Copy-Item '.env.example' '.env' -ErrorAction SilentlyContinue
    Write-Host 'Created .env (default settings)'
}

# Install dependencies
Write-Host ''
Write-Host 'Installing Python dependencies...'
& pip install -r requirements.txt --quiet
Write-Host 'Dependencies installed.'

# Ask about Docker Compose
Write-Host ''
Write-Host 'Start Mosquitto MQTT broker with Docker? (y/n)'
$response = Read-Host
if ($response -eq 'y' -or $response -eq 'Y') {
    $dockerCmd = Get-Command docker-compose -ErrorAction SilentlyContinue
    if ($dockerCmd) {
        Write-Host ''
        Write-Host 'Starting Mosquitto broker...'
        docker-compose up -d
        Write-Host 'Mosquitto started on tcp://localhost:1883'
        Start-Sleep -Seconds 2
    } else {
        Write-Host 'Docker Compose not found. Start MQTT broker manually.'
    }
}

# Start the server
Write-Host ''
Write-Host '========================================='
Write-Host 'Starting Sensor Backend Server...'
Write-Host '========================================='
Write-Host 'Press Ctrl+C to stop the server'
Write-Host ''

& python main.py
