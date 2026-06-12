# Cursor Setup

Cursor can connect to Noru MCP either through direct HTTP configuration or a local stdio bridge.
Prefer OAuth when your Cursor setup supports OAuth for remote MCP servers. Prefer the bridge if your
Cursor setup does not securely store HTTP headers.

## Requirements

- Cursor with MCP support enabled.
- An authenticated Noru MCP connection, using OAuth where supported or a Noru API key for manual
  bearer-token setup.

## OAuth

Use OAuth when Cursor supports OAuth for remote MCP servers. If Cursor already has an authenticated
`noru` MCP connection, the plugin guidance can use that connection in the same Cursor host.

## Direct HTTP With API Key

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

## Stdio Bridge With API Key

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

Do not paste OAuth tokens or API keys into assistant chat. Do not commit `.cursor/` or any config
file containing resolved credentials.

## First Prompt

```text
What order should I do our SOC 2 compliance work in using Noru?
```
