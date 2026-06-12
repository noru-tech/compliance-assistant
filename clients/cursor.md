# Cursor Setup

Cursor can connect to Noru MCP either through direct HTTP configuration or a local stdio bridge.
Prefer the bridge if your Cursor setup does not securely store HTTP headers.

## Requirements

- Cursor with MCP support enabled.
- A Noru API key with least-privilege scopes.

## Direct HTTP

Add this to your private Cursor MCP settings:

```json
{
  "mcpServers": {
    "noru": {
      "url": "https://api.noru.tech/v1/mcp",
      "headers": {
        "Authorization": "Bearer <NORU_API_KEY>"
      }
    }
  }
}
```

Do not commit `.cursor/` or any config file containing the resolved key.

## Stdio Bridge

```json
{
  "mcpServers": {
    "noru": {
      "command": "sh",
      "args": [
        "-lc",
        "exec npx -y mcp-remote@latest \"https://api.noru.tech/v1/mcp\" --header \"Authorization: Bearer ${NORU_API_KEY}\""
      ],
      "env": {
        "NORU_API_KEY": "<NORU_API_KEY>"
      }
    }
  }
}
```

## First Prompt

```text
What order should I do our SOC 2 compliance work in using Noru?
```
