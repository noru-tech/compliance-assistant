# Cursor Setup

Cursor can connect to Noru MCP either through direct HTTP configuration or a local stdio bridge.
Prefer OAuth when your Cursor setup supports OAuth for remote MCP servers. Prefer the bridge if your
Cursor setup does not securely store HTTP headers.

## Cursor Plugin

This repository also uses Cursor's plugin layout. The root `.cursor-plugin/marketplace.json` lists
`plugins/compliance-assistant/`, which has its own `.cursor-plugin/plugin.json`. That manifest
loads the shared `compliance-assistant` skill from `skills/` and registers the `noru` MCP server
from `mcp.json`. The server is remote HTTP at `https://api.noru.tech/v1/mcp` and has no inline
credentials.

Format sources:

- `cursor/plugins` at commit `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e`:
  `schemas/plugin.schema.json`, `schemas/marketplace.schema.json` and, for the local plugin
  directory, `create-plugin/skills/create-plugin-scaffold/SKILL.md`.
- `cursor/plugin-template` at commit `46216072ac5750f782f95bb325b4d12b7c3ae9c9`: `README.md` and
  `docs/add-a-plugin.md`.

The plugin is not yet listed in the Cursor Marketplace. To use it locally, copy
`plugins/compliance-assistant/` to `~/.cursor/plugins/local/compliance-assistant/`. Then
authenticate the `noru` server with OAuth, or set it up as described below.

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
