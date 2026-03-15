#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buddy MCP Server – Bluetooth(시리얼)로 호환 보드와 통신하는 MCP 서버.
환경 변수 BUDDY_PORT 에 시리얼 포트 지정 (예: /dev/cu.USB-Serial 또는 블루투스 SPP 포트).
"""
import asyncio
import json
import os
import subprocess
import sys
import tempfile

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import serial
import serial.tools.list_ports
from mcp.server.fastmcp import FastMCP

from comm.buddy_channel import buddy_channel
from comm.buddy_protocol import BuddyProtocol
from comm.packet_t import packet_t

mcp = FastMCP("Buddy")

_channel = None
_protocol = None


def _get_protocol():
    """연결되어 있으면 protocol 반환, 없으면 연결 시도 후 반환. 실패 시 예외."""
    global _channel, _protocol
    if _protocol is not None and _protocol.running:
        return _protocol
    port = os.environ.get("BUDDY_PORT")
    if not port:
        raise RuntimeError(
            "BUDDY_PORT 환경 변수가 없습니다. "
            "블루투스 동글(시리얼 포트)을 지정하세요. 예: export BUDDY_PORT=/dev/cu.USB-Serial"
        )
    try:
        ser = serial.serial_for_url(port, baudrate=115200, timeout=1)
    except Exception as e:
        raise RuntimeError(f"시리얼 포트를 열 수 없습니다 ({port}): {e}")
    _channel = buddy_channel(ser, BuddyProtocol, packet_t)
    _channel.start()
    _channel._connection_made.wait()
    if not _channel.alive:
        _channel = None
        raise RuntimeError("보드 연결에 실패했습니다.")
    _protocol = _channel.protocol
    return _protocol


def _disconnect():
    global _channel, _protocol
    if _channel is not None:
        try:
            _channel.close()
        except Exception:
            pass
        _channel = None
    _protocol = None


def _find_nrf_port() -> str | None:
    """설명이 'nRF Connect USB CDC' 포함 또는 'nRF'로 시작하는 포트가 있으면 해당 device 경로 반환, 없으면 None."""
    try:
        for p in serial.tools.list_ports.comports():
            desc = (p.description or "").strip()
            lower = desc.lower()
            if "nrf connect usb" in lower or lower.startswith("nrf"):
                return p.device
    except Exception:
        pass
    return None


@mcp.tool()
def buddy_list_ports() -> str:
    """현재 PC에 있는 시리얼(COM) 포트 목록을 반환합니다. Windows는 COM3·COM5, macOS는 /dev/cu.xxx, Linux는 /dev/ttyUSB0 등. 사용자가 동글/보드에 맞는 포트를 골라 buddy_connect(port)에 넣으면 됩니다."""
    try:
        ports = serial.tools.list_ports.comports()
        if not ports:
            return "사용 가능한 시리얼 포트가 없습니다. 동글을 연결했는지 확인하세요."
        lines = []
        for p in ports:
            desc = (p.description or "").strip() or "-"
            lines.append(f"  {p.device}\t{desc}")
        return "사용 가능한 포트:\n" + "\n".join(lines) + "\n\n연결할 때: buddy_connect(port) 에 위 포트 이름(예: COM3, /dev/cu.USB-Serial)을 넣으세요."
    except Exception as e:
        return f"포트 목록 조회 실패: {e}"


@mcp.tool()
def buddy_connect(port: str = "") -> str:
    """보드에 시리얼(블루투스 동글)로 연결합니다. port를 비우거나 'auto'로 하면 nRF Connect USB CDC(또는 설명이 nRF로 시작하는) 포트가 있으면 자동 선택하고, 없으면 포트 목록을 안내합니다. 직접 지정 시: buddy_list_ports()로 확인한 값 사용. Windows: COM3, COM5 / macOS: /dev/cu.xxx / Linux: /dev/ttyUSB0, /dev/ttyACM0"""
    global _channel, _protocol
    _disconnect()
    port = port.strip()
    if not port or port.lower() == "auto":
        auto_port = _find_nrf_port()
        if auto_port:
            port = auto_port
            os.environ["BUDDY_PORT"] = port
            try:
                _get_protocol()
                return f"연결됨: {port} (nRF 자동 선택)"
            except Exception as e:
                return f"연결 실패: {e}"
        # nRF 없음 → 목록 안내
        try:
            ports = serial.tools.list_ports.comports()
            if not ports:
                return "nRF 포트를 찾을 수 없고, 사용 가능한 시리얼 포트도 없습니다. 동글을 연결한 뒤 다시 시도하세요."
            lines = []
            for p in ports:
                desc = (p.description or "").strip() or "-"
                lines.append(f"  {p.device}\t{desc}")
            return "nRF 포트를 찾을 수 없습니다. 아래 목록에서 포트를 골라 buddy_connect(port)에 넣어 주세요.\n\n" + "\n".join(lines)
        except Exception as e:
            return f"포트 목록 조회 실패: {e}"
    os.environ["BUDDY_PORT"] = port
    try:
        _get_protocol()
        return f"연결됨: {port}"
    except Exception as e:
        return f"연결 실패: {e}"


@mcp.tool()
def buddy_disconnect() -> str:
    """보드 연결을 끊습니다."""
    _disconnect()
    return "연결 해제됨"


@mcp.tool()
def buddy_send_dc(dc1: int, dc2: int = 0) -> str:
    """DC 모터 제어. dc1, dc2: 0~255 (0이 정지)."""
    try:
        p = _get_protocol()
        p.sendDC(max(0, min(255, dc1)), max(0, min(255, dc2)))
        return f"DC 전송: dc1={dc1}, dc2={dc2}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def buddy_send_servo(sv1: int, sv2: int = 0) -> str:
    """서보 모터 제어. sv1, sv2: 0~255."""
    try:
        p = _get_protocol()
        p.sendServo(max(0, min(255, sv1)), max(0, min(255, sv2)))
        return f"서보 전송: sv1={sv1}, sv2={sv2}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def buddy_send_io(io: str, value: int) -> str:
    """IO 출력 제어 (LED 등). io: IO1, IO2, IO3, IO4, 3V, 5V 중 하나. value: 0~255."""
    allowed = {"IO1", "IO2", "IO3", "IO4", "3V", "5V"}
    key = io.upper().strip()
    if key not in allowed:
        return f"io는 다음 중 하나여야 합니다: {', '.join(sorted(allowed))}"
    try:
        p = _get_protocol()
        p.sendIO(key, max(0, min(255, value)))
        return f"IO 전송: {key}={value}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def buddy_sensor_config(ultra: int = 0, line1: int = 0, line2: int = 0) -> str:
    """센서 사용 설정. ultra: 초음파(1/0), line1/line2: 라인 센서(1/0)."""
    try:
        p = _get_protocol()
        p.decideToUseSensor(
            1 if ultra else 0,
            1 if line1 else 0,
            1 if line2 else 0,
        )
        return f"센서 설정: ultra={ultra}, line1={line1}, line2={line2}"
    except Exception as e:
        return f"오류: {e}"


def main():
    """MCP 서버를 stdio 전송으로 실행합니다. 로컬 클론에서 run.py 로만 기동합니다."""
    if "--print-mcp-config" in sys.argv:
        project_root = os.path.dirname(os.path.abspath(__file__))
        run_py = os.path.normpath(os.path.join(project_root, "run.py"))
        if os.path.isfile(run_py):
            config = {
                "mcpServers": {
                    "buddy": {
                        "command": "python3",
                        "args": [run_py],
                    }
                }
            }
            print(json.dumps(config, indent=2, ensure_ascii=False))
        else:
            print(
                "이 서버는 pip 설치가 아닌 git 클론에서 run.py 로 실행하는 방식만 지원합니다.\n"
                "프로젝트 루트에서: python3 run.py --print-mcp-config",
                file=sys.stderr,
            )
            sys.exit(1)
        return

    # Claude 등 "원격 MCP 서버 URL"용: SSE 서버로 기동 (URL로 접속 가능)
    if "--sse" in sys.argv:
        port = 8000
        use_https = "--https" in sys.argv
        argv = sys.argv
        for i, a in enumerate(argv):
            if a == "--port" and i + 1 < len(argv):
                try:
                    port = int(argv[i + 1])
                except ValueError:
                    pass
                break
        setattr(mcp.settings, "port", port)

        if use_https:
            # Claude는 HTTPS URL만 허용. 자체 서명 인증서로 로컬 HTTPS 제공
            project_root = os.path.dirname(os.path.abspath(__file__))
            certs_dir = os.path.join(project_root, ".certs")
            os.makedirs(certs_dir, exist_ok=True)
            cert_path = os.path.join(certs_dir, "cert.pem")
            key_path = os.path.join(certs_dir, "key.pem")
            if not os.path.isfile(cert_path) or not os.path.isfile(key_path):
                subprocess.run(
                    [
                        "openssl", "req", "-x509", "-newkey", "rsa:2048",
                        "-keyout", key_path, "-out", cert_path,
                        "-days", "365", "-nodes",
                        "-subj", "/CN=127.0.0.1",
                        "-addext", "subjectAltName=IP:127.0.0.1,DNS:localhost",
                    ],
                    check=True,
                    capture_output=True,
                )
            app = mcp.sse_app()
            import uvicorn
            config = uvicorn.Config(
                app,
                host="127.0.0.1",
                port=port,
                ssl_keyfile=key_path,
                ssl_certfile=cert_path,
                log_level="info",
            )
            server = uvicorn.Server(config)
            print(f"Buddy MCP SSE (HTTPS): https://127.0.0.1:{port}/sse", file=sys.stderr)
            asyncio.run(server.serve())
        else:
            print(f"Buddy MCP SSE: http://127.0.0.1:{port}/sse", file=sys.stderr)
            mcp.run(transport="sse")
        return

    # 터미널에서 직접 실행하면 stdin에 엔터 등이 들어가 JSON 파싱 오류가 나므로 안내 후 종료
    if sys.stdin.isatty():
        print(
            "This server is started by an MCP client (e.g. Cursor), not in a terminal.\n"
            "To get MCP config: python3 run.py --print-mcp-config\n"
            "For Claude (remote URL): python3 run.py --sse [--port 8000]",
            file=sys.stderr,
        )
        sys.exit(0)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
