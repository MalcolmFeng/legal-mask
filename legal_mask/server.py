from __future__ import annotations
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    app.include_router(router)
    return app


def run_server(host: str = "127.0.0.1", port: int = 8765):
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")
