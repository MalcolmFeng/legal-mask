from __future__ import annotations
from legal_mask.types import Annotation, AnnotationStatus, MaskConfig, SensitiveType


class Masker:
    @staticmethod
    def apply(text: str, annotations: list[Annotation], config: MaskConfig | None = None) -> str:
        if config is None:
            config = MaskConfig()

        confirmed = [a for a in annotations if a.status == AnnotationStatus.CONFIRMED]
        if not confirmed:
            return text

        confirmed.sort(key=lambda a: a.start)
        pieces: list[str] = []
        cursor = 0

        for ann in confirmed:
            if ann.sensitive_type not in config.enabled_types:
                continue
            if ann.start > cursor:
                pieces.append(text[cursor:ann.start])

            replacement = config.replacement_map.get(ann.sensitive_type, "[脱敏]")
            if callable(replacement):
                pieces.append(replacement(ann.text))
            else:
                pieces.append(str(replacement))

            cursor = ann.end

        if cursor < len(text):
            pieces.append(text[cursor:])

        return "".join(pieces)
