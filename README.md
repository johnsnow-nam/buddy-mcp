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
      "command": "elio-mcp",
      "env": { "ELIO_PORT": "/dev/cu.YourBluetoothPort" }
    }
  }
}
```

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
| `ELIO_PORT` | 시리얼 포트 경로 (필수). 예: `/dev/cu.USB-Serial`, `COM3` |

Bluetooth SPP로 연결된 경우, OS에서 할당한 시리얼 포트를 지정하면 됩니다.

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
| `elio_connect` | 지정한 시리얼 포트로 엘리오 보드에 연결 |
| `elio_disconnect` | 연결 해제 |
| `elio_send_dc` | DC 모터 제어 (dc1, dc2: 0~255) |
| `elio_send_servo` | 서보 모터 제어 (sv1, sv2: 0~255) |
| `elio_send_io` | IO 출력 제어 (io: IO1~IO4, 3V, 5V / value: 0~255) |
| `elio_sensor_config` | 센서 사용 설정 (ultra, line1, line2: 0 또는 1) |

## MCP 클라이언트 설정

프로젝트 루트에 `mcp-config.example.json`이 있습니다. 아래 중 사용하는 클라이언트에 맞게 **설정 위치**에 `mcpServers` 항목을 추가하세요. `command`, `args`, `env.ELIO_PORT`는 실제 경로와 시리얼 포트로 바꾸면 됩니다.

### Cursor

- **설정 위치**: 프로젝트 `.cursor/mcp.json` 또는 사용자 설정 MCP
- **방법**: `mcp-config.example.json` 내용을 복사해 `mcp.json`의 `mcpServers`에 넣거나, 기존 `mcp.json`에 `elio` 블록만 추가

```json
{
  "mcpServers": {
    "elio": {
      "command": "/절대경로/elio-mcp-server/.venv/bin/python",
      "args": ["/절대경로/elio-mcp-server/server.py"],
      "env": {
        "ELIO_PORT": "/dev/cu.YourBluetoothPort"
      }
    }
  }
}
```

### Claude Desktop

- **설정 위치**
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- **방법**: 위 파일을 연 뒤 `mcpServers` 안에 `elio` 항목을 추가 (이미 `mcpServers`가 있으면 그 안에만 추가)

### 기타 MCP 클라이언트

stdio 기반 MCP를 지원하는 클라이언트라면, 다음만 맞추면 됩니다.

- **command**: 가상환경의 `python` 절대 경로 (macOS/Linux: `프로젝트/.venv/bin/python`, Windows: `프로젝트\\.venv\\Scripts\\python.exe`)
- **args**: `[ "서버의 server.py 절대 경로" ]`
- **env.ELIO_PORT**: 시리얼 포트 (예: macOS `/dev/cu.xxx`, Windows `COM3`)

실행 경로와 `ELIO_PORT`만 실제 환경에 맞게 바꾸면 됩니다.

## PyPI에 배포하기

1. **빌드 도구 설치**
   ```bash
   pip install build twine
   ```

2. **패키지 빌드**
   ```bash
   python -m build
   ```
   `dist/` 폴더에 `.whl`과 `.tar.gz`가 생성됩니다.

3. **PyPI 업로드**
   ```bash
   twine upload dist/*
   ```
   [PyPI](https://pypi.org) 계정으로 로그인하거나, API 토큰을 사용하세요.  
   테스트 업로드는 `twine upload --repository testpypi dist/*` 로 할 수 있습니다.

4. **버전 올리기**  
   `pyproject.toml`의 `version`을 수정한 뒤 다시 빌드·업로드하면 됩니다.

## 참고

- [elio-python](https://github.com/johnsnow-nam/elio-python) 프로젝트의 시리얼·프로토콜 로직을 참고해 구현했습니다.
- 통신: 115200 baud, 패킷 프로토콜(STX/ETX/CRC) 사용.
