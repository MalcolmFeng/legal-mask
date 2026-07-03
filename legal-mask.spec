# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for legal-mask Windows .exe"""

import sys
from pathlib import Path

block_cipher = None

static_dir = Path(__file__).parent / "legal_mask" / "static"
assets = []
if static_dir.exists():
    for f in static_dir.rglob("*"):
        if f.is_file():
            assets.append((str(f), str(f.relative_to(Path(__file__).parent / "legal_mask"))))

a = Analysis(
    ["legal_mask/run.py"],
    pathex=[],
    binaries=[],
    datas=assets,
    hiddenimports=[
        "uvicorn",
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.middleware",
        "uvicorn.middleware.cors",
        "uvicorn.middleware.wsgi",
        "fastapi",
        "pydantic",
        "click",
        "docx",
        "fitz",
        "openpyxl",
        "onnxruntime",
        "transformers",
        "tokenizers",
        "multipart",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="legal-mask",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # no console window on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
