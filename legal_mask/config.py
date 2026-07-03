from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    host: str = "127.0.0.1"
    port: int = 8765
    data_dir: Path = field(default_factory=lambda: Path.home() / ".legal-mask")
    temp_dir: Path = field(default_factory=lambda: Path.home() / ".legal-mask" / "temp")
    db_path: Path = field(default_factory=lambda: Path.home() / ".legal-mask" / "annotations.db")
    model_dir: Path = field(default_factory=lambda: Path.home() / ".legal-mask" / "models")
    cleanup_on_exit: bool = True
    max_upload_size_mb: int = 50

    @classmethod
    def default(cls) -> "Config":
        cfg = cls()
        cfg.data_dir.mkdir(parents=True, exist_ok=True)
        cfg.temp_dir.mkdir(parents=True, exist_ok=True)
        cfg.model_dir.mkdir(parents=True, exist_ok=True)
        return cfg
