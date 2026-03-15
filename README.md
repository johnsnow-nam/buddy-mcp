# Elio MCP Server

**English** | [한국어](README.ko.md)

MCP server for ELIO board over Bluetooth serial (DC motors, servos, IO, sensors).  
Requires Python 3.10+, ELIO board + Bluetooth dongle.

---

## MCP setup (3 steps)

1. **Clone** the repo.
2. In the project folder, run:
   ```bash
   python3 run.py --print-mcp-config
   ```
3. **Paste** the printed JSON into your MCP config (e.g. Cursor `.cursor/mcp.json`, or your client’s `mcpServers`).

Done. The server uses the project’s venv automatically; no global Python path needed.

**Alternative (pip):** `pip install elio-mcp-server` then use `"command": "elio-mcp"` in MCP config.

---

## Tools

| Tool | Purpose |
|------|--------|
| `elio_list_ports` | List COM/serial ports |
| `elio_connect`(port) | Connect to board (pick port from list) |
| `elio_disconnect` | Disconnect |
| `elio_send_dc`, `elio_send_servo`, `elio_send_io`, `elio_sensor_config` | Control motors, IO, sensors |

No `ELIO_PORT` needed: in chat, run **elio_list_ports** → **elio_connect(port)**.

---

한국어: [README.ko.md](README.ko.md)
