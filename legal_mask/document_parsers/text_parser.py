from __future__ import annotations
from pathlib import Path
import uuid
from legal_mask.document_parsers.base import BaseParser
from legal_mask.types import DocumentModel


class TextParser(BaseParser):
    def parse(self, path: Path) -> DocumentModel:
        content = path.read_text(encoding="utf-8")
        return DocumentModel(
            id=str(uuid.uuid4()),
            filename=path.name,
            content=content,
            original_path=str(path),
            file_type="txt",
        )
