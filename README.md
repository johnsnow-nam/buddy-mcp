# Buddy MCP Server

**English** | [한국어](README.ko.md)

MCP server for compatible board over Bluetooth serial (DC motors, servos, IO, sensors).  
Requires Python 3.10+, compatible board + Bluetooth dongle.

**Run from a git clone using the project’s virtual environment.** Clone this repo and run via `run.py` (uses `.venv`, created automatically if missing). Do not use global Python or other envs. **This server is intended for local use only** (config file + stdio).

---

## Local setup (step-by-step) — Windows, macOS, Linux

Use the same steps on all platforms. Only the **config file path** and, on Windows, the **Python command** differ.

### Step 1 — Clone and enter the project

```bash
git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
cd buddy-mcp
```

On **Windows** you can use Command Prompt, PowerShell, or Git Bash.

### Step 2 — Print MCP config JSON

Run this in the project directory. The output is the JSON to add to your config file.

| OS      | Command |
|---------|--------|
| macOS / Linux | `python3 run.py --print-mcp-config` |
| Windows | `python run.py --print-mcp-config` or `py run.py --print-mcp-config` |

Copy the entire JSON output (it includes the correct path to `run.py` for your machine). Example shape:

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

### Step 3 — Config file location

Open (or create) the config file at the path for your OS:

| OS      | Config file path |
|---------|-------------------|
| **macOS**   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` (e.g. `C:\Users\<YourName>\AppData\Roaming\Claude\claude_desktop_config.json`) |
| **Linux**   | `~/.config/Claude/claude_desktop_config.json` |

- To open on **macOS**: `open "$HOME/Library/Application Support/Claude/claude_desktop_config.json"` (quote the path because of the space).
- To open on **Windows**: run `%APPDATA%\Claude\claude_desktop_config.json` in Explorer address bar or use Notepad/VS Code.
- To open on **Linux**: e.g. `xdg-open ~/.config/Claude/claude_desktop_config.json` or edit with your editor.

### Step 4 — Add Buddy MCP to the config file

- If the file is **empty** or does not exist: paste the full JSON from Step 2 as the file content.
- If the file **already has** an `mcpServers` section: merge the `"buddy"` block from Step 2 into that section. Keep valid JSON (no trailing commas). Example with another server:

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

Save the file.

### Step 5 — Restart the client

Restart **Claude Desktop** (or Cursor, if you use `.cursor/mcp.json` in the project instead). The client will start the Buddy MCP server locally via `run.py`.

### Step 6 — Use the tools

In chat:

1. Run **buddy_list_ports** to see serial ports.
2. Run **buddy_connect**(port) with the port you want (e.g. the nRF or COM port). If you leave the port empty or use `"auto"`, a port whose description starts with “nRF” is chosen automatically when available.
3. Then use **buddy_send_dc**, **buddy_send_servo**, **buddy_send_io**, **buddy_sensor_config**, **buddy_disconnect** as needed.

No `BUDDY_PORT` environment variable is required when using **buddy_connect**.

---

## Connection mode (local)

The server runs in **stdio** mode: the client (Claude Desktop, Cursor, etc.) starts `run.py` as a subprocess and talks over stdin/stdout. Do **not** redirect stdout (e.g. `2>&1`)—the client expects only JSON-RPC on stdout.

---

## MCP setup — stdio (Cursor, etc.)

1. **Clone** the repo:
   ```bash
   git clone https://github.com/johnsnow-nam/buddy-mcp.git buddy-mcp
   cd buddy-mcp
   ```
2. **Print MCP config** (uses project `.venv`; creates it if missing). The output contains the correct path to `run.py` for your machine:
   ```bash
   python3 run.py --print-mcp-config
   ```
   If `./run.py` gives "permission denied", use `python3 run.py` instead (or run `chmod +x run.py` once).
3. **Paste** the printed JSON into your MCP config (e.g. Cursor `.cursor/mcp.json`, or your client’s `mcpServers`). Use the output of step 2 as-is; do not use the example path below. Do **not** add `2>&1` or other stdout redirection—the client expects only JSON-RPC on stdout.

**MCP config example** (for reference only; use the JSON from step 2):

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
