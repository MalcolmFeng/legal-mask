from __future__ import annotations
import uuid
import logging
from pathlib import Path
from legal_mask.types import Annotation, AnnotationStatus, SensitiveType
from legal_mask.config import Config

logger = logging.getLogger(__name__)


class NerModel:
    def __init__(self, config: Config | None = None):
        self.config = config or Config.default()
        self._pipeline = None

    def _load_model(self):
        try:
            from transformers import pipeline
            model_path = str(self.config.model_dir / "bert-ner-chinese")
            if Path(model_path).exists():
                self._pipeline = pipeline("ner", model=model_path, tokenizer=model_path)
            else:
                logger.info("NER model not found at %s, downloading...", model_path)
                self._pipeline = pipeline("ner", model="bert-base-chinese", tokenizer="bert-base-chinese")
                self._pipeline.save_pretrained(model_path)
        except Exception as e:
            logger.warning("Failed to load NER model: %s. NER detection will be skipped.", e)
            self._pipeline = None

    def detect(self, text: str) -> list[Annotation]:
        if self._pipeline is None:
            self._load_model()
        if self._pipeline is None:
            return []

        results: list[Annotation] = []
        try:
            ner_results = self._pipeline(text)
            for entity in ner_results:
                stype = self._map_entity_type(entity["entity"])
                if stype:
                    results.append(Annotation(
                        id=str(uuid.uuid4()),
                        doc_id="",
                        sensitive_type=stype,
                        start=entity["start"],
                        end=entity["end"],
                        text=entity["word"],
                        confidence=entity["score"],
                        source="ner",
                        status=AnnotationStatus.PENDING,
                    ))
        except Exception as e:
            logger.error("NER inference failed: %s", e)

        return results

    @staticmethod
    def _map_entity_type(label: str) -> SensitiveType | None:
        label = label.upper()
        if "PER" in label:
            return SensitiveType.PERSON_NAME
        if "ORG" in label:
            return SensitiveType.COMPANY_NAME
        if "LOC" in label:
            return SensitiveType.ADDRESS
        return None
