from pathlib import Path
from legal_mask.document_parsers.base import BaseParser
from legal_mask.document_parsers.docx_parser import DocxParser
from legal_mask.document_parsers.pdf_parser import PdfParser
from legal_mask.document_parsers.excel_parser import ExcelParser
from legal_mask.document_parsers.text_parser import TextParser


def get_parser(path: Path) -> BaseParser:
    ext = path.suffix.lower()
    parsers = {
        ".docx": DocxParser,
        ".pdf": PdfParser,
        ".xlsx": ExcelParser,
        ".txt": TextParser,
        ".md": TextParser,
        ".json": TextParser,
        ".csv": TextParser,
    }
    cls = parsers.get(ext)
    if cls is None:
        raise ValueError(f"Unsupported file type: {ext}")
    return cls()
