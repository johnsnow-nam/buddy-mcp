# Elio MCP Server

[English](README.md) | **한국어**

Bluetooth 시리얼로 ELIO 보드를 제어하는 MCP 서버 (DC 모터, 서보, IO, 센서).  
Python 3.10+, ELIO 보드 + Bluetooth 동글 필요.

---

## MCP 설정 (3단계)

1. 저장소 **클론**
2. 프로젝트 폴더에서 실행:
   ```bash
   python3 run.py --print-mcp-config
   ```
3. 출력된 JSON을 MCP 설정에 **붙여넣기** (예: Cursor `.cursor/mcp.json` 또는 클라이언트의 `mcpServers`)

끝. 서버는 프로젝트 venv를 자동으로 사용하며, 전역 Python 경로는 필요 없습니다.

**pip 사용 시:** `pip install elio-mcp-server` 후 MCP 설정에 `"command": "elio-mcp"` 지정.

---

## 툴

| 툴 | 용도 |
|------|--------|
| `elio_list_ports` | COM/시리얼 포트 목록 |
| `elio_connect`(port) | 보드 연결 (목록에서 포트 선택) |
| `elio_disconnect` | 연결 해제 |
| `elio_send_dc`, `elio_send_servo`, `elio_send_io`, `elio_sensor_config` | 모터·IO·센서 제어 |

`ELIO_PORT` 없이도 됨: 대화에서 **elio_list_ports** → **elio_connect(port)** 실행하면 됨.

---

영문: [README.md](README.md)
