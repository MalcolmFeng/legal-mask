"""Bundled entry point for legal-mask .exe.
Starts the server and opens the browser automatically."""

from __future__ import annotations
import webbrowser
import threading
import time
from legal_mask.server import run_server


def _open_browser(port: int):
    time.sleep(1.5)
    webbrowser.open(f"http://127.0.0.1:{port}")


def main():
    port = 8765
    threading.Thread(target=_open_browser, args=(port,), daemon=True).start()
    run_server(host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
