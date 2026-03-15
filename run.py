#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elio MCP Server launcher (Mac / Windows / Linux 공통).
프로젝트 가상환경(.venv)을 만들고 그 안의 Python으로 server.py를 실행합니다.
MCP 설정: command = python 실행 파일 경로, args = [이 run.py 의 절대 경로]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

def main() -> None:
    project_root = os.path.dirname(os.path.abspath(__file__))
    run_py = os.path.normpath(os.path.abspath(__file__))

    if "--print-mcp-config" in sys.argv:
        config = {
            "mcpServers": {
                "elio": {
                    "command": sys.executable,
                    "args": [run_py],
                }
            }
        }
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return

    venv_dir = os.path.join(project_root, ".venv")
    if sys.platform == "win32":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")

    if not os.path.isfile(python_exe):
        subprocess.run(
            [sys.executable, "-m", "venv", venv_dir],
            check=True,
            cwd=project_root,
        )
        req = os.path.join(project_root, "requirements.txt")
        subprocess.run(
            [python_exe, "-m", "pip", "install", "-r", req, "-q"],
            check=True,
            cwd=project_root,
        )

    server_py = os.path.join(project_root, "server.py")
    os.execv(python_exe, [python_exe, server_py] + [a for a in sys.argv[1:] if a != "--print-mcp-config"])


if __name__ == "__main__":
    main()
