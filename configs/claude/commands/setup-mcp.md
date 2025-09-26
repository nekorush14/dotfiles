---
description: Set up MCP server for this project.
---

# Set up MCP server

Your task is setting up the mcp servers for this project.
You need to setup the following fundamental mcp servers.

- filesystem
- sequential-thinking
- serena
- context7

## Set up flow

You need to run following commands step by steps to setup the mcp servers for Claude Code.

```bash
claude mcp add filesystem --scope project -- npx -y @modelcontextprotocol/server-filesystem
claude mcp add sequential-thinking --scope project -- npx -y @modelcontextprotocol/server-sequential-thinking
claude mcp add serena --scope project -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
claude mcp add context7 --scope project -- npx -y @upstash/context7-mcp
```
