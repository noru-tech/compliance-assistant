# Claude Setup

This repo is installable as a Claude Code plugin and also works with Claude Desktop through a local
MCP bridge.

## Claude Code Plugin

```text
/plugin marketplace add noru-tech/compliance-assistant
/plugin install compliance-assistant@compliance-assistant
```

Then add Noru as an MCP server.

## Claude Code MCP

```bash
export NORU_API_KEY="<your_noru_api_key>"
claude mcp add --transport http noru "https://api.noru.tech/v1/mcp" --header "Authorization: Bearer $NORU_API_KEY"
```

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

## First Prompt

```text
Help me become compliant with ISO 27001 using Noru.
```

The assistant should use live Noru data before recommending next steps.
