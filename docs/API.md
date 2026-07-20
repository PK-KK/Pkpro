# 📡 API Documentation

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "app": "AI IT Technician Assistant"
}
```

### 2. Chat (Q&A)

```
POST /api/chat
```

**Request:**
```json
{
  "question": "ฉันต้องการเปิดพอร์ต 3306 ใน Windows Firewall อย่างไร",
  "language": "th",
  "context": "Optional context information"
}
```

**Response:**
```json
{
  "status": "success",
  "question": "ฉันต้องการเปิดพอร์ต 3306 ใน Windows Firewall อย่างไร",
  "answer": "...",
  "language": "th"
}
```

### 3. Analyze Log

```
POST /api/analyze-log
```

**Request:**
```json
{
  "log_content": "Error: Connection timeout at 10:30:45...",
  "language": "th"
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": "...",
  "language": "th"
}
```

### 4. Generate Script

```
POST /api/generate-script
```

**Request:**
```json
{
  "description": "สร้าง PowerShell script เพื่อบำรุงรักษา Disk Space",
  "script_language": "powershell",
  "language": "th"
}
```

**Response:**
```json
{
  "status": "success",
  "description": "...",
  "script_language": "powershell",
  "script": "...",
  "language": "th"
}
```

### 5. Search Knowledge Base

```
GET /api/knowledge-base/search?query=search_term&category=windows_server
```

**Response:**
```json
{
  "status": "success",
  "query": "search_term",
  "category": "windows_server",
  "results": [...],
  "count": 5
}
```

### 6. Get Knowledge Base Categories

```
GET /api/knowledge-base/categories
```

**Response:**
```json
{
  "status": "success",
  "categories": {
    "windows_server": "Windows Server Tips & Tricks",
    "active_directory": "Active Directory Management",
    ...
  }
}
```

### 7. Add Knowledge Base Article

```
POST /api/knowledge-base/add
```

**Request:**
```json
{
  "category": "windows_server",
  "title": "วิธีเพิ่ม User ใน Windows Server",
  "content": "...",
  "tags": ["user", "management"],
  "language": "th"
}
```

**Response:**
```json
{
  "status": "success",
  "article": {...}
}
```

### 8. Get Model Information

```
GET /api/model-info
```

**Response:**
```json
{
  "status": "success",
  "model": {
    "model": "gemini-2.0-flash",
    "type": "Gemini",
    "status": "active"
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "status": "error"
}
```

## Language Support

- `th` - Thai (ไทย)
- `en` - English

Default language is Thai (`th`).
