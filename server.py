#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elio MCP Server – Bluetooth(시리얼)로 엘리오 보드와 통신하는 MCP 서버.
환경 변수 ELIO_PORT 에 시리얼 포트 지정 (예: /dev/cu.USB-Serial 또는 블루투스 SPP 포트).
"""
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import serial
from mcp.server.fastmcp import FastMCP

from comm.eliochannel import eliochannel
from comm.elioprotocol import ElioProtocol
from comm.packet_t import packet_t

mcp = FastMCP("Elio")

_channel = None
_protocol = None


def _get_protocol():
    """연결되어 있으면 protocol 반환, 없으면 연결 시도 후 반환. 실패 시 예외."""
    global _channel, _protocol
    if _protocol is not None and _protocol.running:
        return _protocol
    port = os.environ.get("ELIO_PORT")
    if not port:
        raise RuntimeError(
            "ELIO_PORT 환경 변수가 없습니다. "
            "블루투스 동글(시리얼 포트)을 지정하세요. 예: export ELIO_PORT=/dev/cu.USB-Serial"
        )
    try:
        ser = serial.serial_for_url(port, baudrate=115200, timeout=1)
    except Exception as e:
        raise RuntimeError(f"시리얼 포트를 열 수 없습니다 ({port}): {e}")
    _channel = eliochannel(ser, ElioProtocol, packet_t)
    _channel.start()
    _channel._connection_made.wait()
    if not _channel.alive:
        _channel = None
        raise RuntimeError("엘리오 보드 연결에 실패했습니다.")
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


@mcp.tool()
def elio_connect(port: str) -> str:
    """엘리오 보드에 시리얼(블루투스 동글)로 연결합니다. port 예: /dev/cu.USB-Serial"""
    global _channel, _protocol
    _disconnect()
    os.environ["ELIO_PORT"] = port
    try:
        _get_protocol()
        return f"연결됨: {port}"
    except Exception as e:
        return f"연결 실패: {e}"


@mcp.tool()
def elio_disconnect() -> str:
    """엘리오 보드 연결을 끊습니다."""
    _disconnect()
    return "연결 해제됨"


@mcp.tool()
def elio_send_dc(dc1: int, dc2: int = 0) -> str:
    """DC 모터 제어. dc1, dc2: 0~255 (0이 정지)."""
    try:
        p = _get_protocol()
        p.sendDC(max(0, min(255, dc1)), max(0, min(255, dc2)))
        return f"DC 전송: dc1={dc1}, dc2={dc2}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def elio_send_servo(sv1: int, sv2: int = 0) -> str:
    """서보 모터 제어. sv1, sv2: 0~255."""
    try:
        p = _get_protocol()
        p.sendServo(max(0, min(255, sv1)), max(0, min(255, sv2)))
        return f"서보 전송: sv1={sv1}, sv2={sv2}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def elio_send_io(io: str, value: int) -> str:
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
def elio_sensor_config(ultra: int = 0, line1: int = 0, line2: int = 0) -> str:
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
    """MCP 서버를 stdio 전송으로 실행합니다 (pip 설치 후 `elio-mcp` 명령으로 호출)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
