# Generic MCP Client Setup

Noru exposes a remote Streamable HTTP MCP endpoint:

```text
https://api.noru.tech/v1/mcp
```

Use bearer authentication:

```text
Authorization: Bearer <NORU_API_KEY>
```

## Environment

```bash
export NORU_API_KEY="<your_noru_api_key>"
export NORU_API_URL="https://api.noru.tech/v1/mcp"
```

## Direct HTTP Clients

Use direct HTTP when your MCP client supports remote Streamable HTTP and secure header storage:

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

## Stdio Bridge Clients

Use `mcp-remote` when your client only supports stdio servers:

```json
{
  "mcpServers": {
    "noru": {
      "command": "sh",
      "args": [
        "-lc",
        "exec npx -y mcp-remote@latest \"${NORU_API_URL:-https://api.noru.tech/v1/mcp}\" --header \"Authorization: Bearer ${NORU_API_KEY}\""
      ],
      "env": {
        "NORU_API_KEY": "<NORU_API_KEY>",
        "NORU_API_URL": "https://api.noru.tech/v1/mcp"
      }
    }
  }
}
```

## Smoke Test

After connecting, verify that your client can:

1. List tools from server `noru`.
2. Read `noru://frameworks/compliance-overview`.
3. Use prompt `assessFrameworkGaps`.

If any step fails with a forbidden or missing tool/resource error, check that the API key has the
required scopes.
