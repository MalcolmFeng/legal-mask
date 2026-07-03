from pathlib import Path
import pytest
from legal_mask.document_parsers import get_parser
from legal_mask.document_parsers.docx_parser import DocxParser
from legal_mask.document_parsers.text_parser import TextParser


def test_text_parser(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("测试内容", encoding="utf-8")
    parser = get_parser(f)
    doc = parser.parse(f)
    assert doc.content == "测试内容"
    assert doc.file_type == "txt"


def test_get_parser_unsupported():
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_parser(Path("test.xyz"))


def test_get_parser_supported():
    assert isinstance(get_parser(Path("test.docx")), DocxParser)
    assert isinstance(get_parser(Path("test.txt")), TextParser)
    assert isinstance(get_parser(Path("test.md")), TextParser)
