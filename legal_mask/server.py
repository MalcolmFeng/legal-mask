from __future__ import annotations
import atexit
import shutil
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

    app.include_router(router)

    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
        index_path = static_dir / "index.html"

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            if full_path.startswith("api/"):
                from fastapi.responses import JSONResponse
                return JSONResponse({"detail": "Not Found"}, status_code=404)
            if index_path.exists():
                return FileResponse(str(index_path))
            return JSONResponse({"detail": "Not Found"}, status_code=404)

    return app


def run_server(host: str = "127.0.0.1", port: int = 8765):
    from legal_mask.config import Config

    cfg = Config.default()
    if cfg.cleanup_on_exit:
        atexit.register(_cleanup_temp)

    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")


def _cleanup_temp():
    from legal_mask.config import Config
    cfg = Config.default()
    if cfg.temp_dir.exists():
        shutil.rmtree(str(cfg.temp_dir), ignore_errors=True)
