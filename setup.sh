#!/bin/bash

# GitLab GenAI Chatbot Setup Script

set -e

echo "🚀 Setting up GitLab GenAI Chatbot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi

# Check Docker (optional)
if ! command -v docker &> /dev/null; then
    print_warning "Docker not found. Docker setup will be skipped."
    DOCKER_AVAILABLE=false
else
    DOCKER_AVAILABLE=true
fi

print_status "Setting up backend..."

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating backend .env file..."
    cp .env.example .env
    print_warning "Please edit backend/.env with your API keys"
fi

# Create data directories
mkdir -p data/chroma_db
mkdir -p logs

cd ..

print_status "Setting up frontend..."

# Frontend setup
cd frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_status "Frontend .env.local already exists"
fi

cd ..

# Create main .env file for Docker
if [ ! -f ".env" ]; then
    print_status "Creating main .env file for Docker..."
    cat > .env << EOF
# API Keys (replace with your actual keys)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
SECRET_KEY=your-secret-key-change-in-production

# Environment
ENVIRONMENT=development
EOF
    print_warning "Please edit .env with your actual API keys"
fi

print_status "Setup completed! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env and backend/.env with your API keys"
echo "2. Run the data scraping: cd backend && python data_processing/scrape_gitlab.py"
echo "3. Create embeddings: python data_processing/create_embeddings.py"
echo "4. Start the backend: uvicorn app.main:app --reload"
echo "5. In another terminal, start the frontend: cd frontend && npm start"
echo ""
echo "Or use Docker:"
echo "docker-compose up --build"
echo ""
echo "Visit http://localhost:3000 to use the chatbot!"
