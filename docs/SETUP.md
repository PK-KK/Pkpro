# 🚀 Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Gemini API Key (free from https://aistudio.google.com/app/apikey)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/PK-KK/Pkpro.git
cd Pkpro
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your Gemini API Key
# nano .env  (Linux/macOS)
# notepad .env  (Windows)
```

Example `.env` content:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
APP_ENV=development
APP_DEBUG=True
APP_PORT=5000
DEFAULT_LANGUAGE=th
```

### 5. Run the Application

```bash
python run.py
```

### 6. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## Troubleshooting

### Issue: "GEMINI_API_KEY is not set"

**Solution:**
1. Check your `.env` file exists
2. Make sure `GEMINI_API_KEY` is properly set
3. Restart the application

### Issue: Port 5000 already in use

**Solution:**
```bash
# Change port in .env file
APP_PORT=5001
```

### Issue: Permission denied on Linux/macOS

**Solution:**
```bash
chmod +x run.py
```

## Next Steps

- Read the [API Documentation](API.md)
- Check [Usage Examples](EXAMPLES.md)
- Join [GitHub Discussions](https://github.com/PK-KK/Pkpro/discussions)
