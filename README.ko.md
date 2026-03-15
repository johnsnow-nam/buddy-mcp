# Buddy MCP Server

[English](README.md) | **한국어**

Bluetooth 시리얼로 호환 보드를 제어하는 MCP 서버 (DC 모터, 서보, IO, 센서).  
Python 3.10+, 호환 보드 + Bluetooth 동글 필요.

**Git에서 클론한 뒤 프로젝트 가상환경(.venv)으로만 구동합니다.** 이 저장소를 클론하고 `run.py`로 실행하며, `run.py`가 `.venv`를 없으면 만들고 그 안에서만 서버를 띄웁니다. 전역 Python이나 다른 env로 실행하지 마세요.

---

## MCP 설정 (Git 클론 후)

1. 저장소 **클론**:
   ```bash
   git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
   cd buddy-mcp
   ```
2. **MCP 설정 출력** (프로젝트 `.venv` 사용, 없으면 자동 생성):
   ```bash
   python3 run.py --print-mcp-config
   ```
3. 출력된 JSON을 MCP 설정에 **붙여넣기** (예: Cursor `.cursor/mcp.json` 또는 클라이언트의 `mcpServers`)

**MCP 설정 예시** (경로는 본인 클론 경로로 바꾸거나, 위 2단계 출력을 그대로 사용):

```json
{
  "mcpServers": {
    "buddy": {
      "command": "python3",
      "args": ["/path/to/buddy-mcp/run.py"]
    }
  }
}
```

MCP가 `run.py`로 서버를 띄우며, `run.py`가 반드시 프로젝트 `.venv` 안에서만 실행되도록 합니다 (전역 Python 사용 안 함).

---

## 툴

| 툴 | 용도 |
|------|--------|
| `buddy_list_ports` | COM/시리얼 포트 목록 |
| `buddy_connect`(port) | 보드 연결 (목록에서 포트 선택) |
| `buddy_disconnect` | 연결 해제 |
| `buddy_send_dc`, `buddy_send_servo`, `buddy_send_io`, `buddy_sensor_config` | 모터·IO·센서 제어 |

`BUDDY_PORT` 없이도 됨: 대화에서 **buddy_list_ports** → **buddy_connect(port)** 실행하면 됨.

---

영문: [README.md](README.md)
