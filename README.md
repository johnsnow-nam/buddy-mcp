# Elio MCP Server

Bluetooth 동글(시리얼)로 엘리오(Elio/LAO) 보드와 연결해, MCP 툴로 DC 모터·서보·IO(LED 등)·센서 설정을 내리는 서버입니다.

## 요구 사항

- Python 3.10+
- 엘리오 보드 + **Bluetooth 동글**(PC와 시리얼 포트로 연결된 상태)
- 시리얼 포트 경로 (예: macOS `/dev/cu.xxx`, Windows `COM3`)

## 설치

### pip으로 설치 (PyPI 배포 후)

```bash
pip install elio-mcp-server
```

설치 후 `elio-mcp` 명령으로 MCP 서버를 실행할 수 있습니다. MCP 클라이언트 설정 시 `command`는 `elio-mcp`, `args`는 비우거나 생략하면 됩니다.

```json
{
  "mcpServers": {
    "elio": {
      "command": "elio-mcp"
    }
  }
}
```
`ELIO_PORT`는 생략해도 됩니다. Claude 등에서는 **elio_list_ports** → **elio_connect(포트이름)** 순으로 연결하면 됩니다. 미리 포트를 알고 있으면 `"env": { "ELIO_PORT": "/dev/cu.YourBluetoothPort" }` 를 넣어도 됩니다.

### 소스에서 설치 (개발/수정 시)

```bash
cd elio-mcp-server
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# 또는 pip install -e .  (에디터블 설치)
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ELIO_PORT` | 시리얼 포트 (선택). 미설정 시 Claude 등에서는 **elio_list_ports**로 포트 목록을 보고 **elio_connect(port)** 로 연결하면 됩니다. |

Windows·Linux·macOS 모두에서 동글을 꽂으면 COM 포트가 생깁니다. 미리 포트를 알고 있으면 `ELIO_PORT`를 설정해 두어도 됩니다.

## 실행

- **pip 설치 후**: `elio-mcp` (환경 변수 `ELIO_PORT` 설정 필요)
- **소스에서**: `python server.py`

```bash
export ELIO_PORT=/dev/cu.YourBluetoothPort
elio-mcp
# 또는: python server.py
```

MCP 클라이언트(Cursor 등)에서는 stdio로 이 프로세스를 실행하도록 설정합니다.

## MCP 툴

| 툴 | 설명 |
|----|------|
| `elio_list_ports` | PC에 있는 시리얼(COM) 포트 목록 반환. Windows: COM3·COM5, macOS: /dev/cu.xxx, Linux: /dev/ttyUSB0 등 |
| `elio_connect` | 지정한 시리얼 포트로 엘리오 보드에 연결 (포트는 elio_list_ports로 확인) |
| `elio_disconnect` | 연결 해제 |
| `elio_send_dc` | DC 모터 제어 (dc1, dc2: 0~255) |
| `elio_send_servo` | 서보 모터 제어 (sv1, sv2: 0~255) |
| `elio_send_io` | IO 출력 제어 (io: IO1~IO4, 3V, 5V / value: 0~255) |
| `elio_sensor_config` | 센서 사용 설정 (ultra, line1, line2: 0 또는 1) |

### Claude 등에서 포트 선택해 연결하기

환경 변수 없이 쓰려면:

1. **elio_list_ports** 를 호출해 사용 가능한 포트 목록을 본다.
2. 사용자가 동글/보드에 해당하는 포트(예: Windows `COM3`, macOS ` /dev/cu.USB-Serial`, Linux ` /dev/ttyUSB0`)를 고른다.
3. **elio_connect(port)** 에 그 포트 이름을 넣어 연결한다.

이후 DC/서보/IO 등 다른 툴을 사용하면 됩니다.

## MCP 클라이언트 설정

이 리포에는 아래 MCP 설정 파일이 들어 있습니다.

| 파일 | 용도 |
|------|------|
| **`.cursor/mcp.json`** | Cursor에서 이 프로젝트를 열면 자동으로 사용. `elio-mcp` 명령 사용 (pip 설치 후) |
| **`mcp-config.example.json`** | 다른 클라이언트에 복사해 쓸 최소 설정 예시 |
| **`mcp-config.from-source.json`** | pip 없이 소스에서 실행할 때용 (경로를 본인 환경에 맞게 수정) |

### Cursor

- 이 프로젝트를 열면 **`.cursor/mcp.json`** 이 적용됩니다. `pip install -e .` 또는 `pip install elio-mcp-server` 로 `elio-mcp`가 PATH에 있으면 그대로 동작합니다.
- 소스만 있고 pip 설치를 안 했다면, `mcp-config.from-source.json` 내용을 `.cursor/mcp.json`에 복사한 뒤 `command`/`args` 경로를 본인 PC 경로로 바꾸세요.

### Claude Desktop

- **설정 위치**
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- **방법**: 위 파일을 연 뒤 `mcpServers` 안에 `elio` 항목을 추가. 내용은 `mcp-config.example.json`을 참고하면 됩니다 (연결 시 포트는 대화 중에 `elio_list_ports` → `elio_connect(port)` 로 선택).

### 기타 MCP 클라이언트

stdio MCP를 지원하는 클라이언트라면 `mcp-config.example.json` 내용을 해당 클라이언트 설정 위치의 `mcpServers`에 넣으면 됩니다. 소스에서 실행하려면 `mcp-config.from-source.json`을 참고해 `command`/`args` 경로만 본인 환경에 맞게 수정하세요.

## PyPI에 배포하기

**계정·API 토큰 등 필요한 정보**는 **[PUBLISHING.md](PUBLISHING.md)** 에 정리해 두었습니다.

요약:

1. **PyPI 계정**  
   [pypi.org](https://pypi.org) 가입 후 **Account settings → API tokens**에서 토큰 발급 (Username: `__token__`, Password: `pypi-...`).

2. **빌드 및 업로드**
   ```bash
   pip install build twine
   python -m build
   twine upload dist/*
   ```

3. **버전**  
   새 배포 시마다 `pyproject.toml`의 `version`을 올린 뒤 다시 빌드·업로드합니다.

## 참고

- [elio-python](https://github.com/johnsnow-nam/elio-python) 프로젝트의 시리얼·프로토콜 로직을 참고해 구현했습니다.
- 통신: 115200 baud, 패킷 프로토콜(STX/ETX/CRC) 사용.
