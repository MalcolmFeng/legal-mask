from __future__ import annotations
from legal_mask.types import Annotation, AnnotationStatus


class Annotator:
    def __init__(self):
        self._annotations: dict[str, list[Annotation]] = {}

    def add_annotation(self, annotation: Annotation):
        doc_id = annotation.doc_id
        if doc_id not in self._annotations:
            self._annotations[doc_id] = []
        self._annotations[doc_id].append(annotation)

    def add_annotations(self, annotations: list[Annotation]):
        for ann in annotations:
            self.add_annotation(ann)

    def get_annotations(self, doc_id: str) -> list[Annotation]:
        return self._annotations.get(doc_id, [])

    def get_annotation(self, annotation_id: str) -> Annotation | None:
        for anns in self._annotations.values():
            for ann in anns:
                if ann.id == annotation_id:
                    return ann
        return None

    def update_status(self, annotation_id: str, status: AnnotationStatus):
        ann = self.get_annotation(annotation_id)
        if ann:
            ann.status = status

    def remove_annotation(self, annotation_id: str):
        for doc_id in list(self._annotations.keys()):
            self._annotations[doc_id] = [a for a in self._annotations[doc_id] if a.id != annotation_id]

    def confirm_all(self, doc_id: str):
        for ann in self._annotations.get(doc_id, []):
            ann.status = AnnotationStatus.CONFIRMED

    def get_pending_count(self, doc_id: str) -> int:
        return sum(1 for a in self._annotations.get(doc_id, []) if a.status == AnnotationStatus.PENDING)
