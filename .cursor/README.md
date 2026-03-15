# MCP 설정 (elio)

`mcp.json`에 있는 경로는 **placeholder**입니다. 그대로 두면 동작하지 않습니다.

**처음 한 번만:** 프로젝트 루트에서 아래를 실행한 뒤, **출력된 내용 전체**로 `mcp.json`을 **통째로 덮어쓰세요**.

```bash
cd /path/to/elio-mcp-server   # 실제 클론한 경로로
python3 run.py --print-mcp-config
```

나온 JSON을 복사해 `.cursor/mcp.json` 파일 내용을 모두 지우고 붙여넣으면 됩니다. (그러면 본인 PC의 Python·run.py 경로가 들어갑니다.)
