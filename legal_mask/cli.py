from __future__ import annotations

import click


@click.group()
def main():
    """legal-mask: 法律文档脱敏系统"""


@main.command()
@click.option("--port", default=8765, help="监听端口")
@click.option("--host", default="127.0.0.1", help="监听地址")
def start(port: int, host: str):
    """启动脱敏系统服务"""
    from legal_mask.server import run_server
    run_server(host=host, port=port)


if __name__ == "__main__":
    main()
