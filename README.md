# 🤖 AI IT Technician Assistant (Pkpro)

> ผู้ช่วยสารพัด สำหรับ IT Technician - วิเคราะห์ปัญหา แนะนำแนวทาง สร้างรายงาน

**Multilingual Support:** Thai 🇹🇭 | English 🇬🇧

---

## 🎯 Features

### Core Functionality
- ✅ **AI-Powered Q&A** - ตอบคำถาม IT ด้วย AI
- ✅ **Log Analysis** - วิเคราะห์ Event Log, Error Logs
- ✅ **Script Generator** - สร้าง PowerShell/Python Scripts
- ✅ **Report Generator** - สร้างรายงาน IT อัตโนมัติ
- ✅ **Knowledge Base** - จัดเก็บ SOP, FAQ, Tips & Tricks
- ✅ **Multilingual** - ภาษาไทย + อังกฤษ

### Specialized Modules
- 🖥️ **Windows Server Analysis** - วิเคราะห์ปัญหา WS
- 🔐 **Active Directory Management** - จัดการ AD
- 🌐 **Network Diagnostics** - ตรวจสอบ Network, DNS, DHCP
- 🔌 **Infrastructure** - Firewall, Switch, CCTV/NVR
- 📊 **M365 Integration** - จัดการ Microsoft 365

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Gemini API Key (ฟรี)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/PK-KK/Pkpro.git
cd Pkpro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your Gemini API Key

# Run the application
python run.py
```

### Access Web Interface
```
http://localhost:5000
```

---

## 📁 Project Structure

```
Pkpro/
├── src/
│   ├── core/
│   │   ├── ai_engine.py          # Gemini API Integration
│   │   ├── knowledge_base.py     # Knowledge Base System
│   │   ├── localization.py       # ไทย/อังกฤษ
│   │   └── __init__.py
│   ├── modules/
│   │   ├── windows_server/       # Windows Server Analysis
│   │   ├── active_directory/     # AD Management
│   │   ├── network/              # Network Tools
│   │   ├── scripts/              # Script Generator
│   │   ├── reports/              # Report Generator
│   │   └── __init__.py
│   ├── integrations/
│   │   ├── gemini_api.py         # Gemini Integration
│   │   ├── microsoft_graph.py    # M365 Integration
│   │   └── __init__.py
│   └── ui/
│       ├── app.py                # Flask App
│       ├── routes.py             # API Routes
│       ├── templates/            # HTML Templates
│       └── static/               # CSS/JS
├── docs/                         # Documentation
├── tests/                        # Unit Tests
├── logs/                         # Application Logs
├── .env.example                  # Environment Template
├── requirements.txt              # Dependencies
├── run.py                        # Entry Point
└── README.md
```

---

## 🔧 Configuration

### 1. Gemini API Key

Get free API key at: https://aistudio.google.com/app/apikey

```bash
# .env file
GEMINI_API_KEY=your_key_here
```

### 2. Language Settings

```bash
# Default: Thai
DEFAULT_LANGUAGE=th  # or 'en' for English
```

---

## 📚 Usage Examples

### 1. Ask Questions (Q&A)
```bash
POST /api/chat
{
  "question": "ฉันต้องการเปิดพอร์ต 3306 ใน Firewall อย่างไร",
  "language": "th"
}
```

### 2. Analyze Logs
```bash
POST /api/analyze-log
{
  "log_content": "[Event Log content here]",
  "language": "th"
}
```

### 3. Generate Scripts
```bash
POST /api/generate-script
{
  "description": "สร้าง PowerShell script เพื่อบำรุงรักษา Disk Space",
  "script_language": "powershell",
  "language": "th"
}
```

### 4. Generate Report
```bash
POST /api/generate-report
{
  "report_type": "network_diagnostic",
  "data": {...},
  "language": "th"
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👨‍💼 Author

**PK-KK** - IT Technician Learning Journey

---

## 📞 Support

For issues and questions:
- 🐛 [GitHub Issues](https://github.com/PK-KK/Pkpro/issues)
- 💬 [GitHub Discussions](https://github.com/PK-KK/Pkpro/discussions)

---

**Built with ❤️ + AI** | Made with Gemini API
