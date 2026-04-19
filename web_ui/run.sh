#!/bin/bash

# Travel Planning Agent - Web UI Startup Script

echo "🚀 Starting Travel Planning Agent Web UI..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the web_ui directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting web server..."
echo "📍 Server will run at: http://localhost:8000"
echo "   Or: http://127.0.0.1:8000"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

# Run the app
python3 app.py
