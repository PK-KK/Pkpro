# การมีส่วนร่วมในโปรเจ็กต์

## 📋 Code of Conduct

โปรเจ็กต์นี้เป็นที่พักพิงให้กับทุกคน โปรด:
- เคารพซึ่งกันและกัน
- ไม่มีการกดขี่หรือการบ骚扰
- ให้การป้อนกลับที่สร้างสรรค์

## 🚀 วิธีการมีส่วนร่วม

### 1. Fork Repository

```bash
click "Fork" button on GitHub
```

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/Pkpro.git
cd Pkpro
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

- Write clean, readable code
- Add comments for complex logic
- Follow PEP 8 style guide for Python
- Test your changes

### 5. Commit Changes

```bash
git add .
git commit -m "ชื่อเรื่อง: คำอธิบายการเปลี่ยนแปลง"
```

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Go to your fork on GitHub
- Click "New Pull Request"
- Add description of changes
- Wait for review

## 📝 Commit Message Format

```
type(scope): subject

body

footer
```

### Types:
- `feat` - ฟีเจอร์ใหม่
- `fix` - แก้ไขบัค
- `docs` - เอกสาร
- `style` - การจัดรูปแบบ
- `refactor` - ปรับปรุงโค้ด
- `test` - เพิ่มการทดสอบ
- `chore` - การบำรุงรักษา

### Example:

```
feat(chat): add AI response streaming

Implement server-sent events for real-time AI responses

Fixes #123
```

## 🧪 Testing

ก่อน submitting PR, โปรดทำการ test:

```bash
pip install -r requirements.txt
pytest tests/
flake8 src/
```

## 📚 Documentation

หากเพิ่มฟีเจอร์ใหม่:
- อัปเดท README.md
- อัปเดท API documentation
- เพิ่ม docstrings ในโค้ด

## ❓ Questions?

- 📝 [GitHub Issues](https://github.com/PK-KK/Pkpro/issues)
- 💬 [GitHub Discussions](https://github.com/PK-KK/Pkpro/discussions)

ขอบคุณที่มีส่วนร่วม! ❤️
