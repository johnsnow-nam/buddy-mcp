# Elio MCP Server

[English](README.md) | **한국어**

Bluetooth 동글(시리얼)로 엘리오(Elio/LAO) 보드와 연결해, MCP 툴로 DC 모터·서보·IO(LED 등)·센서 설정을 내리는 서버입니다.

## 요구 사항

- Python 3.10+
- 엘리오 보드 + **Bluetooth 동글**(PC와 시리얼 포트로 연결된 상태)
- 시리얼 포트 경로 (예: macOS `/dev/cu.xxx`, Windows `COM3`)

## 설치 및 실행 (권장: 가상환경 Launcher, Mac/Windows/Linux 공통)

**사용자 전역 Python/PATH에 구애받지 않고**, 항상 프로젝트 내 가상환경으로만 MCP 서버를 띄우려면 **run.py** 하나만 사용하세요. (Mac, Windows, Linux 동일)

1. 프로젝트를 클론한 뒤, MCP 설정에 `command` = 사용 중인 Python 실행 파일 경로, `args` = **[run.py의 절대 경로]** 를 넣습니다.
2. 첫 실행 시 run.py가 `.venv`가 없으면 자동으로 만들고 `pip install -r requirements.txt`까지 수행합니다.
3. 이후에는 항상 `.venv` 안의 Python으로만 서버가 돌아갑니다.

**설정에 넣을 JSON 확인하기 (모든 OS 동일):**

```bash
# 프로젝트 폴더에서 (Python만 있으면 됨)
python3 run.py --print-mcp-config
# 또는
python run.py --print-mcp-config
```

나온 JSON을 MCP 설정에 그대로 붙여넣으면 됩니다. `command`는 그 PC의 Python 경로, `args`는 run.py 절대 경로로 나옵니다.

### pip으로 설치 (선택)

```bash
pip install elio-mcp-server
```

MCP 설정에 `"command": "elio-mcp"` 만 넣어도 됩니다. (PATH에 있을 때. 못 찾으면 `elio-mcp --print-mcp-config`로 실행 파일 경로를 뽑아서 넣으면 됩니다.)

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

리포에 들어 있는 설정 파일(`.cursor/mcp.json`, `mcp-config.example.json` 등)의 경로는 **placeholder**(`/path/to/elio-mcp-server/run.py`)라서 그대로 쓰면 동작하지 않습니다. **클론한 사람마다 한 번** 아래를 실행해 나온 JSON으로 각자 설정을 채우면 됩니다.

```bash
# 프로젝트 루트에서 (클론한 경로로 이동한 뒤)
python3 run.py --print-mcp-config
```

출력된 JSON을 **그대로** Cursor는 `.cursor/mcp.json`에, Claude 등은 해당 클라이언트 설정 파일의 `mcpServers`에 넣으면 됩니다.

| 파일 | 용도 |
|------|------|
| **`.cursor/mcp.json`** | Cursor용. 위 명령 출력으로 **내용 전체 교체** (자세한 건 `.cursor/README.md` 참고). |
| **`mcp-config.example.json`** | 다른 클라이언트용 예시. 위 명령 출력을 넣거나, `args`만 본인 run.py 절대 경로로 바꾸면 됩니다. |

### Cursor

- `.cursor/mcp.json`은 처음에 placeholder만 들어 있습니다. 프로젝트 루트에서 `python3 run.py --print-mcp-config` 실행 → 출력 전체를 `.cursor/mcp.json`에 붙여넣으면 됩니다.

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
