# Claude Setup

This repository installs as a Claude Code plugin. It also works with Claude Desktop through a local
MCP bridge.

## Claude Code plugin

```text
/plugin marketplace add noru-tech/compliance-assistant
/plugin install compliance-assistant@compliance-assistant
```

The plugin includes the `noru` MCP server (`https://api.noru.tech/v1/mcp`), so you don't add it
yourself. Installing doesn't sign you in to Noru or store any credentials.

## Sign in with OAuth (recommended)

1. Run `/mcp`.
2. Select `noru`, listed as `plugin:compliance-assistant:noru`.
3. Choose **Authenticate** and finish the sign-in in your browser.

Claude Code stores the token and refreshes it for you. To check the connection, ask:

```text
Check my Noru connection.
```

The `noru-setup` skill reports the organization, your scopes, and any toolsets you might want to add.
You can also run it directly as `/compliance-assistant:noru-setup`.

## API key (headless or CI)

Use this only when OAuth isn't possible. Add your own `noru` server at user scope. The skills work
with either server. You can disable the plugin's unauthenticated copy in `/mcp` so only one is
listed:

```bash
export NORU_API_KEY="<your_noru_api_key>"
claude mcp add --scope user --transport http noru "https://api.noru.tech/v1/mcp" --header "Authorization: Bearer $NORU_API_KEY"
```

To limit the connection to certain toolsets, add `?toolsets=controls,policies,evidence,risks` to the
URL.

## Claude Desktop

Claude Desktop commonly uses a stdio bridge for remote MCP servers. Add this to your private
`claude_desktop_config.json` and keep the file out of git:

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

Replace `<NORU_API_KEY>` only in your private local config.

Don't paste OAuth tokens or API keys into assistant chat. Don't commit local Claude configuration
files that contain resolved credentials.

## First prompts

```text
What should we do next for SOC 2?
Where are our biggest ISO 27001 gaps?
Are we ready for our audit? What would an auditor flag first?
```

The assistant reads your live Noru data before it recommends next steps.
