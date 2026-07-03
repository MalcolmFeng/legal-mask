from __future__ import annotations
from pathlib import Path
import uuid
import fitz
from legal_mask.document_parsers.base import BaseParser
from legal_mask.types import DocumentModel


class PdfParser(BaseParser):
    def parse(self, path: Path) -> DocumentModel:
        doc = fitz.open(str(path))
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        parts = []
        for i, page_text in enumerate(pages):
            if i > 0:
                parts.append(f"\n--- 第{i + 1}页 ---\n")
            parts.append(page_text)
        content = "".join(parts)
        return DocumentModel(
            id=str(uuid.uuid4()),
            filename=path.name,
            content=content,
            original_path=str(path),
            file_type="pdf",
        )
