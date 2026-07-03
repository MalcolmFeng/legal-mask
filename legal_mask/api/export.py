from __future__ import annotations
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from legal_mask.config import Config
from legal_mask.types import DocumentModel, MaskConfig
from legal_mask.engine.exporter import Exporter
from legal_mask.api.documents import annotator

router = APIRouter()
config = Config.default()


@router.get("/{doc_id}")
async def export_document(doc_id: str):
    from legal_mask.api.documents import _documents

    doc_meta = _documents.get(doc_id)
    if not doc_meta:
        raise HTTPException(status_code=404, detail="Document not found")

    annotations = annotator.get_annotations(doc_id)
    doc = DocumentModel(
        id=doc_id,
        filename=doc_meta["filename"],
        content=doc_meta["content"],
        original_path=doc_meta["temp_path"],
        file_type=doc_meta["file_type"],
    )

    output_path = config.temp_dir / f"masked_{doc_id}.docx"

    try:
        Exporter.export_docx(doc, annotations, str(output_path))
    except Exception:
        text_result = Exporter.export_text(doc, annotations)
        output_path = config.temp_dir / f"masked_{doc_id}.txt"
        output_path.write_text(text_result, encoding="utf-8")

    return FileResponse(
        str(output_path),
        filename=f"masked_{doc_meta['filename']}",
        media_type="application/octet-stream",
    )


@router.get("/text/{doc_id}")
async def export_text(doc_id: str):
    from legal_mask.api.documents import _documents

    doc_meta = _documents.get(doc_id)
    if not doc_meta:
        raise HTTPException(status_code=404, detail="Document not found")

    annotations = annotator.get_annotations(doc_id)
    doc = DocumentModel(
        id=doc_id,
        filename=doc_meta["filename"],
        content=doc_meta["content"],
        original_path=doc_meta["temp_path"],
        file_type=doc_meta["file_type"],
    )

    text_result = Exporter.export_text(doc, annotations)
    return {"masked_text": text_result}


@router.get("/comparison/{doc_id}")
async def export_comparison(doc_id: str):
    from legal_mask.api.documents import _documents

    doc_meta = _documents.get(doc_id)
    if not doc_meta:
        raise HTTPException(status_code=404, detail="Document not found")

    annotations = annotator.get_annotations(doc_id)
    doc = DocumentModel(
        id=doc_id,
        filename=doc_meta["filename"],
        content=doc_meta["content"],
        original_path=doc_meta["temp_path"],
        file_type=doc_meta["file_type"],
    )

    comparison = Exporter.export_comparison(doc, annotations)
    return {"comparison": comparison}
