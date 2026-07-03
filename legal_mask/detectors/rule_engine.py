from __future__ import annotations

import re
import uuid

from legal_mask.types import Annotation, AnnotationStatus, SensitiveType


class RuleEngine:
    @staticmethod
    def _valid_id_card(s: str) -> bool:
        if len(s) != 18:
            return False
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_chars = "10X98765432"
        try:
            total = sum(int(s[i]) * weights[i] for i in range(17))
            return s[17].upper() == check_chars[total % 11]
        except (ValueError, IndexError):
            return False

    def __init__(self):
        self.patterns: list[tuple[re.Pattern, SensitiveType, str, bool]] = [
            (re.compile(r"(?<!\d)(1[3-9]\d{9})(?!\d)"), SensitiveType.PHONE, "rule", False),
            (re.compile(r"([（(]\d{4}[）)][\u4e00-\u9fa5\d]+[民刑行执调保破]_?\w{0,4}\d+号)"), SensitiveType.CASE_NUMBER, "rule", False),
            (re.compile(r"(?<!\d)([1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)"), SensitiveType.ID_CARD, "rule", True),
            (re.compile(r"(?<!\d)([1-9]\d{2}[1-6]\d{2}(?=.*[A-Z])[0-9A-HJ-NPQRTUWXY]{11}[0-9A-HJ-NPQRTUWXY])(?!\d)"), SensitiveType.CREDIT_CODE, "rule", False),
            (re.compile(r"(?<![A-Za-z0-9])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})(?![A-Za-z])"), SensitiveType.EMAIL, "rule", False),
            (re.compile(r"(?<!\d)(\d{16,17}|\d{19})(?!\d)"), SensitiveType.BANK_ACCOUNT, "rule", False),
        ]

    def detect(self, text: str) -> list[Annotation]:
        results: list[Annotation] = []
        seen_ranges: set[tuple[int, int]] = set()

        for pattern, stype, source, validate in self.patterns:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                matched_text = match.group(1)
                if validate and stype == SensitiveType.ID_CARD:
                    if not self._valid_id_card(matched_text):
                        continue
                if self._is_overlapping(start, end, seen_ranges):
                    continue
                seen_ranges.add((start, end))
                results.append(Annotation(
                    id=str(uuid.uuid4()),
                    doc_id="",
                    sensitive_type=stype,
                    start=start,
                    end=end,
                    text=matched_text,
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
