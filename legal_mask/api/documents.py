from __future__ import annotations
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from legal_mask.config import Config
from legal_mask.document_parsers import get_parser
from legal_mask.detectors.rule_engine import RuleEngine
from legal_mask.detectors.keyword_matcher import KeywordMatcher
from legal_mask.detectors.ner_model import NerModel
from legal_mask.engine.annotator import Annotator
from legal_mask.types import AnnotationStatus

router = APIRouter()
config = Config.default()
rule_engine = RuleEngine()
keyword_matcher = KeywordMatcher()
ner_model = NerModel(config)
annotator = Annotator()

_documents: dict[str, dict] = {}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    max_bytes = config.max_upload_size_mb * 1024 * 1024
    if file.size and file.size > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max: {config.max_upload_size_mb}MB")

    file_id = str(uuid.uuid4())
    temp_path = config.temp_dir / f"{file_id}_{file.filename}"

    try:
        content = await file.read()
        temp_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        parser = get_parser(temp_path)
        doc = parser.parse(temp_path)
        doc.id = file_id
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    rule_results = rule_engine.detect(doc.content)
    keyword_results = keyword_matcher.detect(doc.content)
    ner_results = ner_model.detect(doc.content)

    all_annotations = rule_results + keyword_results + ner_results
    for ann in all_annotations:
        ann.doc_id = file_id

    annotator.add_annotations(all_annotations)

    _documents[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "file_type": doc.file_type,
        "content": doc.content,
        "temp_path": str(temp_path),
    }

    return {
        "id": file_id,
        "filename": file.filename,
        "file_type": doc.file_type,
        "content_length": len(doc.content),
        "annotations": [ann.__dict__ for ann in all_annotations],
        "annotation_count": len(all_annotations),
    }


@router.get("")
async def list_documents():
    return [
        {"id": d["id"], "filename": d["filename"], "file_type": d["file_type"]}
        for d in _documents.values()
    ]


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    doc = _documents.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    annotations = annotator.get_annotations(doc_id)
    return {
        **doc,
        "annotations": [ann.__dict__ for ann in annotations],
    }
