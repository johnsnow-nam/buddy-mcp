# Elio MCP Server

**English** | [한국어](README.ko.md)

MCP server for controlling an Elio/LAO board over Bluetooth serial: DC motors, servos, IO (e.g. LEDs), and sensor configuration.

## Requirements

- Python 3.10+
- Elio board + **Bluetooth dongle** (connected to the PC as a serial port)
- Serial port path (e.g. macOS `/dev/cu.xxx`, Windows `COM3`)

## Install and run (recommended: venv launcher, Mac/Windows/Linux)

To run the MCP server **only** inside the project’s virtual environment (no dependency on the user’s global Python or PATH), use the single **run.py** script on all platforms.

1. Clone the repo, then set MCP config: `command` = path to your Python executable, `args` = **[absolute path to run.py]**.
2. On first run, `run.py` creates `.venv` if missing and runs `pip install -r requirements.txt`.
3. The server then always runs with the Python inside `.venv`.

**Get the JSON for your MCP config (same on all OSes):**

```bash
# From the project folder (Python only is required)
python3 run.py --print-mcp-config
# or
python run.py --print-mcp-config
```

Paste the printed JSON into your MCP config. It will contain your Python path and the absolute path to `run.py`.

### Install via pip (optional)

```bash
pip install elio-mcp-server
```

Use `"command": "elio-mcp"` in MCP config (when it’s on PATH). If the client can’t find it, run `elio-mcp --print-mcp-config` and use the printed config.

## Environment variables

| Variable   | Description |
|-----------|-------------|
| `ELIO_PORT` | Serial port (optional). If unset, use **elio_list_ports** then **elio_connect(port)** in Claude etc. |

Plugging in the dongle creates a COM/serial port on Windows, Linux, and macOS. You can set `ELIO_PORT` if you already know it.

## Running

- **After pip install:** run `elio-mcp` (set `ELIO_PORT` if needed).
- **From source:** run `python server.py`.

```bash
export ELIO_PORT=/dev/cu.YourBluetoothPort
elio-mcp
# or: python server.py
```

MCP clients (e.g. Cursor) should run this process via stdio.

## MCP tools

| Tool | Description |
|------|-------------|
| `elio_list_ports` | List serial (COM) ports on the PC (e.g. COM3, COM5 on Windows; /dev/cu.xxx on macOS; /dev/ttyUSB0 on Linux). |
| `elio_connect` | Connect to the Elio board on the given serial port (use `elio_list_ports` to see ports). |
| `elio_disconnect` | Disconnect. |
| `elio_send_dc` | DC motor control (dc1, dc2: 0–255). |
| `elio_send_servo` | Servo control (sv1, sv2: 0–255). |
| `elio_send_io` | IO output (io: IO1–IO4, 3V, 5V; value: 0–255). |
| `elio_sensor_config` | Sensor config (ultra, line1, line2: 0 or 1). |

### Choosing the port in Claude etc.

Without setting `ELIO_PORT`:

1. Call **elio_list_ports** to see available ports.
2. User picks the port for the dongle/board (e.g. Windows `COM3`, macOS `/dev/cu.USB-Serial`, Linux `/dev/ttyUSB0`).
3. Call **elio_connect(port)** with that port name.

Then use the other tools as needed.

## MCP client configuration

The config files in the repo (e.g. `.cursor/mcp.json`, `mcp-config.example.json`) use a **placeholder** path (`/path/to/elio-mcp-server/run.py`) and won’t work as-is. **Once per clone**, run the command below and use the printed JSON to fill your config.

```bash
# From the project root (after cloning)
python3 run.py --print-mcp-config
```

Paste the output into `.cursor/mcp.json` (Cursor) or into your client’s `mcpServers` (e.g. Claude). See `.cursor/README.md` for Cursor details.

| File | Purpose |
|------|---------|
| **`.cursor/mcp.json`** | Cursor. Replace its contents with the command output above. |
| **`mcp-config.example.json`** | Example for other clients. Use the command output or set `args` to your `run.py` path. |

### Cursor

- `.cursor/mcp.json` starts with a placeholder. From the project root, run `python3 run.py --print-mcp-config` and paste the full output into `.cursor/mcp.json`.

### Claude Desktop

- **Config path:**  
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`  
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Add an `elio` entry under `mcpServers` (see `mcp-config.example.json`). Choose the port in chat via **elio_list_ports** → **elio_connect(port)**.

### Other MCP clients

Put the contents of `mcp-config.example.json` into your client’s `mcpServers`. Adjust `command` and `args` for your environment if running from source.

## Publishing to PyPI

See **[PUBLISHING.md](PUBLISHING.md)** for account, API token, and upload steps.

Summary:

1. **PyPI account** – Register at [pypi.org](https://pypi.org), create an API token under Account settings → API tokens (Username: `__token__`, Password: `pypi-...`).
2. **Build and upload:**  
   `pip install build twine` → `python -m build` → `twine upload dist/*`
3. **Version** – Bump `version` in `pyproject.toml` before each new upload.

## References

- Protocol and serial logic are based on [elio-python](https://github.com/johnsnow-nam/elio-python).
- Communication: 115200 baud, STX/ETX/CRC packet protocol.
