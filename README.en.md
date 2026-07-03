# legal-mask · Legal Document Redaction System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4%2B-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org)

A locally-deployed, semi-automated sensitive information redaction tool designed for Chinese legal documents. Upload a document → auto-detect sensitive information → review and confirm → export the redacted result. All data stays on your machine.

> 🇨🇳 中文版 README 请见 [README.md](README.md)

## Features

- **Multi-engine detection** — rule-based regex, keyword matching, and NER model
- **Broad coverage** — personal names, ID numbers, phone numbers, case numbers, court names, company names, unified social credit codes, addresses, emails, bank accounts, judges/clerk info, custom tags
- **Human review** — web interface to confirm, ignore, or modify each annotation
- **Manual annotation** — select text directly in the document to mark sensitive info
- **Format-preserving export** — DOCX retains original formatting; also supports TXT and side-by-side comparison
- **100% local** — no internet required, data never leaves your machine
- **Standalone binary** — Windows users can run the pre-built `.exe`

## Quick Start

### Option 1: pip install

```bash
pip install legal-mask
legal-mask start
# Open http://127.0.0.1:8765 in your browser
```

### Option 2: Run from source

```bash
git clone https://github.com/malcolmfeng/legal-mask.git
cd legal-mask

# Backend
pip install -r requirements.txt
python -m legal_mask start

# Frontend (optional, for development with hot-reload)
cd legal_mask/frontend
npm install
npm run dev
```

### Option 3: Windows standalone binary

Download `legal-mask.exe` from the [Releases](https://github.com/malcolmfeng/legal-mask/releases) page and double-click to run. The browser will open automatically.

## Test Document

The repository includes a sample document `examples/测试文档-法律文书脱敏测试.docx` containing various types of sensitive information. Upload it directly to test the system's detection and redaction capabilities.

## Supported Document Formats

| Format | Parser | Import | Export |
|--------|--------|--------|--------|
| DOCX   | python-docx | ✓ | ✓ (format-preserving) |
| PDF    | PyMuPDF | ✓ | ✓ |
| XLSX   | openpyxl | ✓ | ✓ |
| TXT    | — | ✓ | ✓ |

## Detection Engines

| Engine | Method | Covered Types | Confidence |
|--------|--------|---------------|------------|
| Rule Engine | Regex + checksum | ID card, phone, case number, credit code, email, bank account | High (0.95) |
| Keyword Matcher | Legal keywords + role patterns | Judge, assistant, clerk, parties, court name | Medium-High (0.85–0.9) |
| NER Model | Transformers / ONNX | Person name, organization, address | Medium (model-dependent) |

## Workflow

1. **Upload** — drag-and-drop or file picker
2. **Auto-detect** — system scans and annotates sensitive information
3. **Review** — confirm, ignore, or modify each annotation via the web UI
4. **Manual annotate** — select text in the document to add custom annotations
5. **Export** — download the redacted DOCX/TXT, or view a side-by-side comparison with the original

## Project Structure

```
legal-mask/
├── legal_mask/
│   ├── api/              # REST API (FastAPI)
│   ├── detectors/        # Detection engines (rule, keyword, NER)
│   ├── document_parsers/ # Document parsers (DOCX, PDF, XLSX, TXT)
│   ├── engine/           # Annotation management, masking, export
│   ├── frontend/         # Vue.js 3 frontend source
│   ├── static/           # Built frontend assets
│   ├── cli.py            # CLI entry point
│   ├── server.py         # Server bootstrap
│   ├── config.py         # Configuration
│   └── types.py          # Type definitions
├── examples/             # Sample documents
├── tests/                # Test suite
├── build.py              # Windows .exe build script
└── pyproject.toml
```

## Configuration

Config is stored in `~/.legal-mask/` and can be adjusted via the Settings page:

- Listen address and port (default `127.0.0.1:8765`)
- Upload size limit (default 50MB)
- Enabled sensitive information types
- Custom replacement rules

## Build Windows Executable

```bash
python build.py
# Output: dist/legal-mask.exe
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Frontend dev (hot-reload)
cd legal_mask/frontend && npm run dev

# Build frontend
cd legal_mask/frontend && npm run build
```

## Tech Stack

**Backend:** Python, FastAPI, Uvicorn, Click  
**Frontend:** Vue.js 3, TypeScript, Vite, Pinia, Vue Router  
**Document Processing:** python-docx, PyMuPDF, openpyxl  
**ML Inference:** ONNX Runtime, Transformers  
**Packaging:** PyInstaller  

## License

MIT
