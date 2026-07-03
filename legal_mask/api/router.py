from __future__ import annotations
from fastapi import APIRouter
from legal_mask.api.documents import router as docs_router
from legal_mask.api.annotations import router as ann_router
from legal_mask.api.export import router as export_router
from legal_mask.api.settings import router as settings_router

router = APIRouter(prefix="/api")
router.include_router(docs_router, prefix="/documents", tags=["documents"])
router.include_router(ann_router, prefix="/annotations", tags=["annotations"])
router.include_router(export_router, prefix="/export", tags=["export"])
router.include_router(settings_router, prefix="/settings", tags=["settings"])


@router.get("/health")
async def health():
    return {"status": "ok"}
