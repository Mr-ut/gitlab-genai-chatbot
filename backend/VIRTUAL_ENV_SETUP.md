# Virtual Environment Setup Guide

## 🐍 Setting Up Python Virtual Environment for Backend

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# On some systems, you might need to use:
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**

```bash
source venv/bin/activate
```

**On Windows:**

```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

### Step 4: Verify Virtual Environment

```bash
# Check Python path (should point to venv)
which python

# Check pip path
which pip

# Your terminal prompt should show (venv) at the beginning
```

### Step 5: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### Step 6: Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env
# or
code .env
```

### Step 7: Create Data Directories

```bash
mkdir -p data/chroma_db
mkdir -p logs
```

### Step 8: Run Data Processing (Optional)

```bash
# Scrape GitLab data
python data_processing/scrape_gitlab.py

# Create embeddings
python data_processing/create_embeddings.py
```

### Step 9: Start the Backend Server

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with specific host/port
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 10: Test the Backend

```bash
# In another terminal, test the API
curl http://localhost:8000/api/v1/health

# Or visit in browser:
# http://localhost:8000/docs (API documentation)
# http://localhost:8000/api/v1/health (health check)
```

## 🔧 Virtual Environment Management

### Deactivate Virtual Environment

```bash
deactivate
```

### Remove Virtual Environment

```bash
# Delete the venv directory
rm -rf venv
```

### Recreate Virtual Environment

```bash
# If you need to start fresh
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Environment Variables Required

Edit your `.env` file with these values:

```bash
# At least one API key is required
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-key-here

# Other optional configurations
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./chatbot.db
```

## 🚨 Troubleshooting

### Python Not Found

```bash
# Try different Python commands
python3 --version
python --version

# Install Python if needed (macOS)
brew install python3
```

### Permission Errors

```bash
# On macOS, you might need to use
python3 -m venv venv
```

### Import Errors

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

## ✅ Verification Checklist

- [ ] Virtual environment created
- [ ] Virtual environment activated (prompt shows `(venv)`)
- [ ] Dependencies installed
- [ ] `.env` file configured with API keys
- [ ] Data directories created
- [ ] Backend server starts without errors
- [ ] Health check endpoint responds

## 🎯 Quick Start Commands

```bash
# Complete setup in one go
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
mkdir -p data/chroma_db logs
uvicorn app.main:app --reload
```
