# Buddy MCP Server

[English](README.md) | **한국어**

Bluetooth 시리얼로 호환 보드를 제어하는 MCP 서버 (DC 모터, 서보, IO, 센서).  
Python 3.10+, 호환 보드 + Bluetooth 동글 필요.

**Git에서 클론한 뒤 프로젝트 가상환경(.venv)으로만 구동합니다.** 이 저장소를 클론하고 `run.py`로 실행하며, `run.py`가 `.venv`를 없으면 만들고 그 안에서만 서버를 띄웁니다. 전역 Python이나 다른 env로 실행하지 마세요. **로컬 전용** (설정 JSON 파일 + stdio)으로 사용합니다.

---

## 로컬 사용법 (단계별) — Windows, macOS, Linux

Windows·macOS·Linux 모두 같은 순서로 진행합니다. **설정 파일 경로**와, Windows에서만 **Python 실행 명령**이 다릅니다.

### 1단계 — 저장소 클론 및 이동

```bash
git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
cd buddy-mcp
```

**Windows**에서는 명령 프롬프트, PowerShell, Git Bash 중 하나 사용하면 됩니다.

### 2단계 — MCP 설정 JSON 출력

프로젝트 폴더에서 아래 명령을 실행합니다. 출력되는 JSON을 설정 파일에 넣을 내용입니다.

| OS | 명령 |
|----|------|
| macOS / Linux | `python3 run.py --print-mcp-config` |
| Windows | `python run.py --print-mcp-config` 또는 `py run.py --print-mcp-config` |

출력된 JSON 전체를 복사합니다 (본인 PC의 `run.py` 경로가 이미 들어 있습니다). 형식 예:

```json
{
  "mcpServers": {
    "buddy": {
      "command": "python3",
      "args": ["/absolute/path/to/buddy-mcp/run.py"]
    }
  }
}
```

### 3단계 — 설정 파일 위치

사용 중인 OS에 맞는 경로에서 설정 파일을 엽니다 (없으면 만듦).

| OS | 설정 파일 경로 |
|----|----------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` (예: `C:\Users\<사용자명>\AppData\Roaming\Claude\claude_desktop_config.json`) |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

- **macOS**에서 열기: `open "$HOME/Library/Application Support/Claude/claude_desktop_config.json"` (경로에 공백이 있으므로 반드시 따옴표로 감싸기).
- **Windows**에서 열기: 탐색기 주소창에 `%APPDATA%\Claude\claude_desktop_config.json` 입력하거나 메모장/VS Code로 열기.
- **Linux**에서 열기: `xdg-open ~/.config/Claude/claude_desktop_config.json` 또는 원하는 에디터로 열기.

### 4단계 — 설정 파일에 Buddy MCP 추가

- 파일이 **비어 있거나 없음**: 2단계에서 복사한 JSON 전체를 붙여넣고 저장.
- 이미 **mcpServers**가 있음: 2단계 출력에서 `"buddy"` 블록만 복사해 `mcpServers` 안에 추가. JSON 문법 유지 (마지막 항목 뒤 쉼표 금지). 예:

```json
{
  "mcpServers": {
    "other-server": { ... },
    "buddy": {
      "command": "python3",
      "args": ["/path/to/buddy-mcp/run.py"]
    }
  }
}
```

저장합니다.

### 5단계 — 클라이언트 재시작

**Claude Desktop** (또는 Cursor를 쓰면 해당 프로젝트의 `.cursor/mcp.json` 사용 시 Cursor)을 다시 실행합니다. 클라이언트가 로컬에서 `run.py`로 Buddy MCP 서버를 띄웁니다.

### 6단계 — 도구 사용

채팅에서:

1. **buddy_list_ports** 로 시리얼 포트 목록 확인.
2. **buddy_connect**(port) 에 사용할 포트 지정 (nRF 또는 COM 포트). port를 비우거나 `"auto"`로 하면 설명이 "nRF"로 시작하는 포트가 있으면 자동 선택됩니다.
3. 이후 **buddy_send_dc**, **buddy_send_servo**, **buddy_send_io**, **buddy_sensor_config**, **buddy_disconnect** 등을 필요에 따라 사용.

**buddy_connect**를 쓰면 `BUDDY_PORT` 환경 변수는 따로 설정하지 않아도 됩니다.

---

## 연결 방식 (로컬)

**stdio** 방식으로 동작합니다. 클라이언트(Claude Desktop, Cursor 등)가 `run.py`를 프로세스로 실행하고 stdin/stdout으로 통신합니다. stdout 리다이렉트(예: `2>&1`)는 사용하지 마세요. 클라이언트는 stdout에 JSON-RPC만 오는 것을 기대합니다.

---

## MCP 설정 — stdio (Cursor 등)

1. 저장소 **클론**:
   ```bash
   git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
   cd buddy-mcp
   ```
2. **MCP 설정 출력** (프로젝트 `.venv` 사용, 없으면 자동 생성). 출력된 JSON에 본인 환경에 맞는 `run.py` 경로가 들어 있습니다:
   ```bash
   python3 run.py --print-mcp-config
   ```
   (`./run.py`로 실행 시 "permission denied"가 나오면 `chmod +x run.py` 후 다시 시도하거나, `python3 run.py`를 사용하세요.)
3. 출력된 JSON을 MCP 설정에 **그대로 붙여넣기** (예: Cursor `.cursor/mcp.json` 또는 클라이언트의 `mcpServers`). 아래 예시 경로가 아니라 2단계에서 나온 JSON을 사용하세요. stdout 리다이렉트(예: `2>&1`)는 넣지 마세요. 클라이언트는 stdout에 JSON-RPC만 오는 것을 기대합니다.

**MCP 설정 예시** (참고용; 실제로는 2단계 출력을 그대로 사용):

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
