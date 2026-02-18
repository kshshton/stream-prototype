#!/bin/bash
# Quick start script for the sensor backend server

set -e

echo "========================================="
echo "Sensor Backend Server - Quick Start"
echo "========================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

echo "✓ Python found: $(python --version)"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

echo "✓ pip found"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created (using default settings)"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# Ask about Docker Compose
echo ""
echo "Do you want to start Mosquitto MQTT broker with Docker? (y/n)"
read -r response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    if command -v docker-compose &> /dev/null; then
        echo ""
        echo "Starting Mosquitto broker..."
        docker-compose up -d
        echo "✓ Mosquitto started on tcp://localhost:1883"
        sleep 2
    else
        echo "Docker Compose not found. Please start your MQTT broker manually."
    fi
fi

# Start the server
echo ""
echo "========================================="
echo "Starting Sensor Backend Server..."
echo "========================================="
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
