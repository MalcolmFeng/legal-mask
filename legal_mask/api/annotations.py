from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from legal_mask.api.documents import annotator
from legal_mask.types import Annotation, AnnotationStatus, SensitiveType
import uuid

router = APIRouter()


class StatusUpdate(BaseModel):
    status: str


class ManualAnnotation(BaseModel):
    doc_id: str
    start: int
    end: int
    text: str
    sensitive_type: str


@router.put("/{ann_id}/status")
async def update_annotation_status(ann_id: str, update: StatusUpdate):
    try:
        status = AnnotationStatus(update.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {update.status}")
    annotator.update_status(ann_id, status)
    ann = annotator.get_annotation(ann_id)
    if ann:
        return ann.__dict__
    raise HTTPException(status_code=404, detail="Annotation not found")


@router.put("/confirm-all/{doc_id}")
async def confirm_all(doc_id: str):
    annotator.confirm_all(doc_id)
    annotations = annotator.get_annotations(doc_id)
    return {"annotations": [ann.__dict__ for ann in annotations]}


@router.post("")
async def add_manual_annotation(ann: ManualAnnotation):
    try:
        stype = SensitiveType(ann.sensitive_type)
    except ValueError:
        stype = SensitiveType.CUSTOM
    new_ann = Annotation(
        id=str(uuid.uuid4()),
        doc_id=ann.doc_id,
        sensitive_type=stype,
        start=ann.start,
        end=ann.end,
        text=ann.text,
        confidence=1.0,
        source="manual",
        status=AnnotationStatus.CONFIRMED,
    )
    annotator.add_annotation(new_ann)
    return new_ann.__dict__


@router.delete("/{ann_id}")
async def remove_annotation(ann_id: str):
    annotator.remove_annotation(ann_id)
    return {"status": "deleted"}


@router.get("/pending-count/{doc_id}")
async def get_pending_count(doc_id: str):
    return {"pending_count": annotator.get_pending_count(doc_id)}
