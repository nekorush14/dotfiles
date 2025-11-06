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
- codex-mcp

## Command Arguments

This command accepts optional arguments to skip specific MCP servers:

- `--skip-filesystem`: Skip filesystem server installation
- `--skip-sequential-thinking`: Skip sequential-thinking server installation
- `--skip-serena`: Skip serena server installation
- `--skip-context7`: Skip context7 server installation
- `--skip-codex-mcp`: Skip codex-mcp server installation
- `--skip-all`: Skip all installations (dry-run mode)

Example usage:

- `/setup-mcp --skip-filesystem --skip-serena` - Install only sequential-thinking, context7, and codex-mcp
- `/setup-mcp --skip-all` - Don't install anything, just show what would be installed

## Set up flow

You need to run following commands step by steps to setup the mcp servers for Claude Code.

**IMPORTANT INSTRUCTIONS**:

1. First, check if any arguments were provided (e.g., `--skip-<server-name>`)
2. Before running each command, check if:
   - The corresponding `--skip-<server-name>` argument was provided
   - OR the MCP server is already setup by running `claude mcp list`
3. Only run the command if both conditions are false (not skipped and not already setup)
4. If `--skip-all` is provided, list all servers that would be installed but don't install any

**Setup commands**:

```bash
# filesystem
claude mcp add filesystem --scope project -- npx -y @modelcontextprotocol/server-filesystem

# sequential-thinking
claude mcp add sequential-thinking --scope project -- npx -y @modelcontextprotocol/server-sequential-thinking

# serena
claude mcp add serena --scope project -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)

# context7
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# codex-mcp
claude mcp add codex-mcp codex mcp-server
```
