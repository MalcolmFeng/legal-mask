"""Build legal-mask as a standalone executable.
Usage: python build.py
"""

from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
STATIC = ROOT / "legal_mask" / "static"
ENTRY = ROOT / "legal_mask" / "run.py"


def build():
    if not STATIC.exists() or not list(STATIC.iterdir()):
        print("Building frontend first...")
        subprocess.run(["npx", "vite", "build"], cwd=str(ROOT / "legal_mask" / "frontend"), check=True)
        subprocess.run(["cp", "-r", str(ROOT / "legal_mask" / "frontend" / "dist"), str(STATIC)], check=True)

    print("Building executable with PyInstaller...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "legal-mask",
        "--onefile",
        "--windowed",
        "--add-data", f"{STATIC}{os.pathsep}legal_mask/static",
        "--hidden-import", "uvicorn",
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "fastapi",
        "--hidden-import", "pydantic",
        "--hidden-import", "click",
        "--hidden-import", "docx",
        "--hidden-import", "fitz",
        "--hidden-import", "openpyxl",
        "--hidden-import", "onnxruntime",
        "--collect-all", "onnxruntime",
        str(ENTRY),
    ]
    subprocess.run(cmd, check=True)
    print(f"\nDone! Executable at: {ROOT / 'dist' / 'legal-mask.exe'}")


if __name__ == "__main__":
    build()
