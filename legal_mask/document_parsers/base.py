from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from legal_mask.types import DocumentModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, path: Path) -> DocumentModel:
        pass
