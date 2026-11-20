# Generic MCP Client Setup

Noru exposes a remote Streamable HTTP MCP endpoint:

```text
https://api.noru.tech/v1/mcp
```

Authentication is managed by your MCP host or client, not by this plugin. If your client already has
an authenticated `noru` MCP connection, the assistant can use it in that same host.

For a new connection, use one authentication path:

- OAuth, when your MCP client supports OAuth for remote MCP servers.
- A Noru API key, when your client needs manual bearer-token or headless configuration.

Both paths send a bearer credential to Noru MCP:

```text
Authorization: Bearer <access_token_or_api_key>
```

## API Key Environment

```bash
export NORU_API_KEY="<your_noru_api_key>"
```

## Direct HTTP Clients With API Key

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

## Stdio Bridge Clients With API Key

Use `mcp-remote` when your client only supports stdio servers:

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

## Smoke Test

After connecting, verify that your client can:

1. List tools from server `noru`.
2. Call `getMcpCapabilities`. It returns the organization, granted scopes, the tools this
   connection exposes, and which toolsets are active.
3. Read `noru://frameworks/compliance-overview`.

If a tool or resource is missing or forbidden, compare the scopes and toolsets in the
`getMcpCapabilities` result with
[the scope and toolset reference](../plugins/compliance-assistant/skills/compliance-assistant/references/scopes-and-toolsets.md).
