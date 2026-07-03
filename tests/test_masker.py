from legal_mask.engine.masker import Masker
from legal_mask.types import Annotation, AnnotationStatus, SensitiveType, MaskConfig
import uuid


def make_annotation(stype: SensitiveType, start: int, end: int, text: str, status=AnnotationStatus.CONFIRMED):
    return Annotation(
        id=str(uuid.uuid4()),
        doc_id="test",
        sensitive_type=stype,
        start=start,
        end=end,
        text=text,
        confidence=1.0,
        source="test",
        status=status,
    )


def test_mask_person_name():
    text = "原告张三"
    anns = [make_annotation(SensitiveType.PERSON_NAME, 2, 4, "张三")]
    result = Masker.apply(text, anns)
    assert result == "原告[姓名]"


def test_mask_id_card():
    text = "身份证110101199003151234"
    anns = [make_annotation(SensitiveType.ID_CARD, 3, 21, "110101199003151234")]
    result = Masker.apply(text, anns)
    assert result == "身份证110101********1234"


def test_mask_phone():
    text = "电话13800138000"
    anns = [make_annotation(SensitiveType.PHONE, 2, 13, "13800138000")]
    result = Masker.apply(text, anns)
    assert result == "电话138****8000"


def test_mask_multiple():
    text = "张三110101199003151234"
    anns = [
        make_annotation(SensitiveType.PERSON_NAME, 0, 2, "张三"),
        make_annotation(SensitiveType.ID_CARD, 2, 20, "110101199003151234"),
    ]
    result = Masker.apply(text, anns)
    assert result == "[姓名]110101********1234"


def test_skips_pending_annotations():
    text = "张三"
    anns = [make_annotation(SensitiveType.PERSON_NAME, 0, 2, "张三", AnnotationStatus.PENDING)]
    result = Masker.apply(text, anns)
    assert result == "张三"


def test_skips_ignored_annotations():
    text = "张三"
    anns = [make_annotation(SensitiveType.PERSON_NAME, 0, 2, "张三", AnnotationStatus.IGNORED)]
    result = Masker.apply(text, anns)
    assert result == "张三"


def test_custom_replacement():
    text = "张三"
    anns = [make_annotation(SensitiveType.PERSON_NAME, 0, 2, "张三")]
    config = MaskConfig()
    config.replacement_map[SensitiveType.PERSON_NAME] = "***"
    result = Masker.apply(text, anns, config)
    assert result == "***"
