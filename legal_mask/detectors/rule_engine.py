from __future__ import annotations

import re
import uuid
from typing import Any

from legal_mask.types import Annotation, AnnotationStatus, SensitiveType


class RuleEngine:
    def __init__(self):
        self.patterns: list[tuple[re.Pattern, SensitiveType, str]] = [
            (re.compile(r"(?<!\d)(\d{6}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)"), SensitiveType.ID_CARD, "rule"),
            (re.compile(r"(?<!\d)(1[3-9]\d{9})(?!\d)"), SensitiveType.PHONE, "rule"),
            (re.compile(r"[（(]\d{4}[）)][\u4e00-\u9fa5\d]+[民刑行执调保破]_?\w{0,4}\d+号"), SensitiveType.CASE_NUMBER, "rule"),

            (re.compile(r"(?<!\d)([1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)"), SensitiveType.ID_CARD, "rule"),

            (re.compile(r"(?<!\d)([1-9]\d{2}[1-6]\d{2}[0-9A-HJ-NPQRTUWXY]{11}[0-9A-HJ-NPQRTUWXY])(?!\d)"), SensitiveType.CREDIT_CODE, "rule"),

            (re.compile(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"), SensitiveType.EMAIL, "rule"),

            (re.compile(r"(?<!\d)(\d{16,19})(?!\d)"), SensitiveType.BANK_ACCOUNT, "rule"),
        ]

    def detect(self, text: str) -> list[Annotation]:
        results: list[Annotation] = []
        seen_ranges: set[tuple[int, int]] = set()

        for pattern, stype, source in self.patterns:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                if self._is_overlapping(start, end, seen_ranges):
                    continue
                seen_ranges.add((start, end))
                results.append(Annotation(
                    id=str(uuid.uuid4()),
                    doc_id="",
                    sensitive_type=stype,
                    start=start,
                    end=end,
                    text=match.group(0),
                    confidence=0.95,
                    source=source,
                    status=AnnotationStatus.PENDING,
                ))

        results.sort(key=lambda a: a.start)
        return results

    def _is_overlapping(self, start: int, end: int, seen: set[tuple[int, int]]) -> bool:
        for s, e in seen:
            if not (end <= s or start >= e):
                return True
        return False
