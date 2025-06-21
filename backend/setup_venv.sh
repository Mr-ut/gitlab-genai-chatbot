#!/bin/bash

# Backend Virtual Environment Setup Script
set -e

echo "🐍 Setting up Python Virtual Environment for GitLab GenAI Chatbot Backend"
echo ""

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "Usage: cd backend && ./setup_venv.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 first"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Verify activation
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created (please edit with your API keys)"
else
    echo "⚙️ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/chroma_db
mkdir -p logs

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   code .env"
echo ""
echo "2. Activate the virtual environment (in future sessions):"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the backend server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Optional - Process GitLab data:"
echo "   python data_processing/scrape_gitlab.py"
echo "   python data_processing/create_embeddings.py"
echo ""
echo "🌐 API will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
