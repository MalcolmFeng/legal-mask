from __future__ import annotations
import re
import uuid
from legal_mask.types import Annotation, AnnotationStatus, SensitiveType


class KeywordMatcher:
    def __init__(self):
        self.patterns: list[tuple[str, SensitiveType]] = [
            (r"(审判长|审判员|代理审判员|人民陪审员)[：:，,\s;；]\s*([\u4e00-\u9fa5]{2,4})", SensitiveType.JUDGE),
            (r"(法官助理)[：:]\s*([\u4e00-\u9fa5]{2,4})", SensitiveType.JUDGE_ASSISTANT),
            (r"(书记员)[：:]\s*([\u4e00-\u9fa5]{2,4})", SensitiveType.CLERK),
            (r"(公诉人|辩护人|诉讼代理人|委托诉讼代理人|法定代表人)[：:]\s*([\u4e00-\u9fa5]{2,4})", SensitiveType.PERSON_NAME),
        ]
        self.court_pattern = re.compile(
            r"[\u4e00-\u9fa5]{2,}(?:省|市|区|县|自治[区县])(?:第[一二三四五六七八九十]+)?(?:高级|中级|初级)?人民法院"
        )
        self.judge_position = re.compile(
            r"(?:审判长|审判员|代理审判员|人民陪审员)\s+(\S{2,4})"
        )

    def detect(self, text: str) -> list[Annotation]:
        results: list[Annotation] = []

        for pattern, stype in self.patterns:
            for match in re.finditer(pattern, text):
                full_start = match.start()
                name_start = match.start(2)
                name_end = match.end(2)
                results.append(Annotation(
                    id=str(uuid.uuid4()),
                    doc_id="",
                    sensitive_type=stype,
                    start=name_start,
                    end=name_end,
                    text=match.group(2),
                    confidence=0.9,
                    source="keyword",
                    status=AnnotationStatus.PENDING,
                ))

        for match in self.court_pattern.finditer(text):
            results.append(Annotation(
                id=str(uuid.uuid4()),
                doc_id="",
                sensitive_type=SensitiveType.COURT_NAME,
                start=match.start(),
                end=match.end(),
                text=match.group(0),
                confidence=0.85,
                source="keyword",
                status=AnnotationStatus.PENDING,
            ))

        results.sort(key=lambda a: a.start)
        return results
