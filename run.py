#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buddy MCP Server launcher (Mac / Windows / Linux 공통).
프로젝트 가상환경(.venv)을 만들고 그 안의 Python으로 server.py를 실행합니다.
MCP 설정: command = python 실행 파일 경로, args = [이 run.py 의 절대 경로]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

def main() -> None:
    # 실행 중인 run.py 기준으로 경로 계산 (어디서 실행하든 동일한 절대 경로)
    _run_py_abs = os.path.abspath(os.path.realpath(__file__))
    project_root = os.path.dirname(_run_py_abs)
    run_py = os.path.normpath(_run_py_abs)

    if "--print-mcp-config" in sys.argv:
        # 로컬 클론 전용: 실행 중인 run.py 절대 경로를 기준으로 설정 출력
        config = {
            "mcpServers": {
                "buddy": {
                    "command": "python3",
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
        # pip 업그레이드 안내가 stdout으로 나오면 MCP 스트림이 깨지므로 비활성화
        env = os.environ.copy()
        env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        subprocess.run(
            [python_exe, "-m", "pip", "install", "-r", req, "-q"],
            check=True,
            cwd=project_root,
            env=env,
        )

    server_py = os.path.join(project_root, "server.py")
    os.execv(python_exe, [python_exe, server_py] + [a for a in sys.argv[1:] if a != "--print-mcp-config"])


if __name__ == "__main__":
    main()
