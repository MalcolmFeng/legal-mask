from __future__ import annotations
import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from legal_mask.config import Config
from legal_mask.types import SensitiveType

router = APIRouter()
config = Config.default()
_settings_path = config.data_dir / "settings.json"


class SettingsData(BaseModel):
    enabled_types: list[str]
    mask_format: str


def _load_settings() -> dict:
    if _settings_path.exists():
        try:
            return json.loads(_settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"enabled_types": [t.value for t in SensitiveType], "mask_format": "default"}


def _save_settings(data: dict):
    _settings_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@router.get("")
async def get_settings():
    return _load_settings()


@router.put("")
async def update_settings(data: SettingsData):
    settings = {"enabled_types": data.enabled_types, "mask_format": data.mask_format}
    _save_settings(settings)
    return settings
