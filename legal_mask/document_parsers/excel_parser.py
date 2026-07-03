from __future__ import annotations
from pathlib import Path
import uuid
import openpyxl
from legal_mask.document_parsers.base import BaseParser
from legal_mask.types import DocumentModel


class ExcelParser(BaseParser):
    def parse(self, path: Path) -> DocumentModel:
        wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
        lines = []
        for sheet in wb.worksheets:
            lines.append(f"[Sheet: {sheet.title}]")
            for row in sheet.iter_rows(values_only=True):
                cells = [str(c) if c is not None else "" for c in row]
                lines.append("\t".join(cells))
        wb.close()
        content = "\n".join(lines)
        return DocumentModel(
            id=str(uuid.uuid4()),
            filename=path.name,
            content=content,
            original_path=str(path),
            file_type="xlsx",
        )
