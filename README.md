# Buddy MCP Server

**English** | [한국어](README.ko.md)

MCP server for compatible board over Bluetooth serial (DC motors, servos, IO, sensors).  
Requires Python 3.10+, compatible board + Bluetooth dongle.

**Run from a git clone using the project’s virtual environment.** The server is intended to be used by cloning this repo and running via `run.py`, which uses the project’s `.venv` (created automatically if missing). Do not run with global Python or other envs.

---

## MCP setup (from git clone)

1. **Clone** the repo:
   ```bash
   git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
   cd buddy-mcp
   ```
2. **Print MCP config** (uses project `.venv`; creates it if missing):
   ```bash
   python3 run.py --print-mcp-config
   ```
3. **Paste** the printed JSON into your MCP config (e.g. Cursor `.cursor/mcp.json`, or your client’s `mcpServers`).

**MCP config example** (replace the path with your actual clone path, or use the output of step 2):

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

MCP starts the server via `run.py`; `run.py` ensures the server runs inside the project’s `.venv` only (no global Python).

---

## Tools

| Tool | Purpose |
|------|--------|
| `buddy_list_ports` | List COM/serial ports |
| `buddy_connect`(port) | Connect to board (pick port from list) |
| `buddy_disconnect` | Disconnect |
| `buddy_send_dc`, `buddy_send_servo`, `buddy_send_io`, `buddy_sensor_config` | Control motors, IO, sensors |

No `BUDDY_PORT` needed: in chat, run **buddy_list_ports** → **buddy_connect(port)**.

---

한국어: [README.ko.md](README.ko.md)
