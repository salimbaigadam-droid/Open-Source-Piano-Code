#!/bin/bash

# Quick Start Script for Piano Synthesizer
# This script helps you quickly start any backend

echo "╔══════════════════════════════════════════════════╗"
echo "║  🎹 Chromatic Cascade - Piano Synthesizer       ║"
echo "║  Quick Start Menu                               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Choose which backend to start:"
echo ""
echo "1) Frontend Only (Tone.js - no backend needed)"
echo "2) Python Backend (Port 8000)"
echo "3) Go Backend (Port 8001)"
echo "4) Rust Backend (Port 8002)"
echo "5) All Backends"
echo "6) Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "Opening frontend in browser..."
        echo "No backend needed - using Tone.js for audio synthesis"
        if command -v xdg-open > /dev/null; then
            xdg-open frontend/piano.html
        elif command -v open > /dev/null; then
            open frontend/piano.html
        else
            echo "Please open frontend/piano.html in your browser"
        fi
        ;;
    2)
        echo "Starting Python Backend..."
        cd backend-python
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        source venv/bin/activate
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo "Starting server on http://localhost:8000"
        python main.py
        ;;
    3)
        echo "Starting Go Backend..."
        cd backend-go
        echo "Downloading dependencies..."
        go mod download
        echo "Starting server on http://localhost:8001"
        go run main.go
        ;;
    4)
        echo "Starting Rust Backend..."
        cd backend-rust
        echo "Building (this may take a while first time)..."
        cargo build --release
        echo "Starting server on http://localhost:8002"
        cargo run --release
        ;;
    5)
        echo "Starting all backends..."
        echo "This will open 3 terminal windows"
        
        # Python
        gnome-terminal -- bash -c "cd backend-python && source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py; exec bash"
        
        # Go
        gnome-terminal -- bash -c "cd backend-go && go run main.go; exec bash"
        
        # Rust
        gnome-terminal -- bash -c "cd backend-rust && cargo run --release; exec bash"
        
        echo "All backends starting in separate terminals..."
        echo "Backends will be available at:"
        echo "  - Python: http://localhost:8000"
        echo "  - Go:     http://localhost:8001"
        echo "  - Rust:   http://localhost:8002"
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
