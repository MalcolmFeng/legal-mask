from __future__ import annotations
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from legal_mask.api.router import router


def create_app() -> FastAPI:
    app = FastAPI(title="legal-mask", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    app.include_router(router)
    return app


def run_server(host: str = "127.0.0.1", port: int = 8765):
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")
