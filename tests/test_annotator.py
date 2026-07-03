from legal_mask.engine.annotator import Annotator
from legal_mask.types import Annotation, AnnotationStatus, SensitiveType


def test_add_and_get():
    ann = Annotation(id="1", doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                     start=0, end=2, text="张三", confidence=1.0, source="test")
    annotator = Annotator()
    annotator.add_annotation(ann)
    results = annotator.get_annotations("doc1")
    assert len(results) == 1
    assert results[0].text == "张三"


def test_update_status():
    ann = Annotation(id="1", doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                     start=0, end=2, text="张三", confidence=1.0, source="test")
    annotator = Annotator()
    annotator.add_annotation(ann)
    annotator.update_status("1", AnnotationStatus.CONFIRMED)
    results = annotator.get_annotations("doc1")
    assert results[0].status == AnnotationStatus.CONFIRMED


def test_remove_annotation():
    ann = Annotation(id="1", doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                     start=0, end=2, text="张三", confidence=1.0, source="test")
    annotator = Annotator()
    annotator.add_annotation(ann)
    annotator.remove_annotation("1")
    results = annotator.get_annotations("doc1")
    assert len(results) == 0


def test_get_annotations_doc_filter():
    annotator = Annotator()
    ann1 = Annotation(id="1", doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                      start=0, end=2, text="张三", confidence=1.0, source="test")
    ann2 = Annotation(id="2", doc_id="doc2", sensitive_type=SensitiveType.PHONE,
                      start=0, end=11, text="13800138000", confidence=1.0, source="test")
    annotator.add_annotation(ann1)
    annotator.add_annotation(ann2)
    assert len(annotator.get_annotations("doc1")) == 1
    assert len(annotator.get_annotations("doc2")) == 1


def test_add_manual_annotation():
    annotator = Annotator()
    ann = Annotation(id="manual1", doc_id="doc1", sensitive_type=SensitiveType.CUSTOM,
                     start=5, end=10, text="机密内容", confidence=1.0, source="manual")
    annotator.add_annotation(ann)
    results = annotator.get_annotations("doc1")
    assert results[0].source == "manual"


def test_confirm_all():
    annotator = Annotator()
    for i in range(3):
        ann = Annotation(id=str(i), doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                         start=i, end=i+1, text=f"x{i}", confidence=1.0, source="test")
        annotator.add_annotation(ann)
    annotator.confirm_all("doc1")
    results = annotator.get_annotations("doc1")
    assert all(r.status == AnnotationStatus.CONFIRMED for r in results)


def test_get_pending_count():
    annotator = Annotator()
    for i in range(3):
        ann = Annotation(id=str(i), doc_id="doc1", sensitive_type=SensitiveType.PERSON_NAME,
                         start=i, end=i+1, text=f"x{i}", confidence=1.0, source="test")
        annotator.add_annotation(ann)
    annotator.update_status("0", AnnotationStatus.CONFIRMED)
    assert annotator.get_pending_count("doc1") == 2
