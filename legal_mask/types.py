from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SensitiveType(str, Enum):
    PERSON_NAME = "person_name"
    ID_CARD = "id_card"
    PHONE = "phone"
    CASE_NUMBER = "case_number"
    COURT_NAME = "court_name"
    COMPANY_NAME = "company_name"
    CREDIT_CODE = "credit_code"
    ADDRESS = "address"
    EMAIL = "email"
    BANK_ACCOUNT = "bank_account"
    JUDGE = "judge"
    JUDGE_ASSISTANT = "judge_assistant"
    CLERK = "clerk"
    CUSTOM = "custom"


SENSITIVE_TYPE_LABELS: dict[SensitiveType, str] = {
    SensitiveType.PERSON_NAME: "姓名",
    SensitiveType.ID_CARD: "身份证号",
    SensitiveType.PHONE: "手机号",
    SensitiveType.CASE_NUMBER: "案号",
    SensitiveType.COURT_NAME: "法院名称",
    SensitiveType.COMPANY_NAME: "企业名称",
    SensitiveType.CREDIT_CODE: "统一社会信用代码",
    SensitiveType.ADDRESS: "地址",
    SensitiveType.EMAIL: "邮箱",
    SensitiveType.BANK_ACCOUNT: "银行账户",
    SensitiveType.JUDGE: "审判法官",
    SensitiveType.JUDGE_ASSISTANT: "法官助理",
    SensitiveType.CLERK: "书记员",
    SensitiveType.CUSTOM: "自定义",
}

SENSITIVE_TYPE_COLORS: dict[SensitiveType, str] = {
    SensitiveType.PERSON_NAME: "#FF6B6B",
    SensitiveType.ID_CARD: "#4ECDC4",
    SensitiveType.PHONE: "#45B7D1",
    SensitiveType.CASE_NUMBER: "#96CEB4",
    SensitiveType.COURT_NAME: "#9B59B6",
    SensitiveType.COMPANY_NAME: "#F39C12",
    SensitiveType.CREDIT_CODE: "#1ABC9C",
    SensitiveType.ADDRESS: "#E67E22",
    SensitiveType.EMAIL: "#3498DB",
    SensitiveType.BANK_ACCOUNT: "#E74C3C",
    SensitiveType.JUDGE: "#8E44AD",
    SensitiveType.JUDGE_ASSISTANT: "#2C3E50",
    SensitiveType.CLERK: "#7F8C8D",
    SensitiveType.CUSTOM: "#95A5A6",
}


class AnnotationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IGNORED = "ignored"
    MODIFIED = "modified"


@dataclass
class Annotation:
    id: str
    doc_id: str
    sensitive_type: SensitiveType
    start: int
    end: int
    text: str
    confidence: float
    source: str  # "rule" or "ner" or "keyword" or "manual"
    status: AnnotationStatus = AnnotationStatus.PENDING
    note: str = ""


@dataclass
class DocumentModel:
    id: str
    filename: str
    content: str
    original_path: str
    file_type: str  # "docx", "pdf", "xlsx", "txt"


@dataclass
class MaskConfig:
    replacement_map: dict[SensitiveType, str] = field(default_factory=lambda: {
        SensitiveType.PERSON_NAME: "[姓名]",
        SensitiveType.ID_CARD: lambda s: s[:6] + "********" + s[-4:],
        SensitiveType.PHONE: lambda s: s[:3] + "****" + s[-4:],
        SensitiveType.CASE_NUMBER: "[案号]",
        SensitiveType.COURT_NAME: "[法院]",
        SensitiveType.COMPANY_NAME: "[企业名称]",
        SensitiveType.CREDIT_CODE: lambda s: s[:2] + "********" + s[-4:],
        SensitiveType.ADDRESS: "[地址]",
        SensitiveType.EMAIL: "[邮箱]",
        SensitiveType.BANK_ACCOUNT: "[银行账户]",
        SensitiveType.JUDGE: "[审判法官]",
        SensitiveType.JUDGE_ASSISTANT: "[法官助理]",
        SensitiveType.CLERK: "[书记员]",
        SensitiveType.CUSTOM: "[脱敏]",
    })
    enabled_types: set[SensitiveType] = field(default_factory=lambda: set(SensitiveType))
