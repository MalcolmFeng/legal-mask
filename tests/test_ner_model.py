import pytest
from legal_mask.detectors.ner_model import NerModel


def test_ner_model_placeholder():
    model = NerModel()
    model._load_model()
    assert model._pipeline is None, "Model should not load in test without model file"


def test_ner_detect_empty():
    model = NerModel()
    results = model.detect("这是一个测试。")
    assert isinstance(results, list)
