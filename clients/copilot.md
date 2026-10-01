# GitHub Copilot CLI Setup

GitHub Copilot CLI reads Claude-style plugin marketplaces. It looks for `marketplace.json` in
`.claude-plugin/`, which is where this repository keeps its marketplace. It also loads plugins whose
manifest is `.claude-plugin/plugin.json`. No Copilot-specific files are needed.

Sources: `github/docs` at commit `10844e10c034b5e5d9b62793c3af9feb4b91de07`, in
`content/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing.md`,
`plugins-marketplace.md`, `data/reusables/copilot/copilot-cli/cli-claude-plugin-dir.md` and
`content/copilot/reference/copilot-cli-reference/cli-plugin-reference.md` ("File locations").

## Install

```bash
copilot plugin marketplace add noru-tech/compliance-assistant
copilot plugin install compliance-assistant@compliance-assistant
```

In an interactive session you can run the same commands as `/plugin marketplace add ...` and
`/plugin install ...`.

## Authentication

The plugin's MCP configuration registers the `noru` server at `https://api.noru.tech/v1/mcp`
without credentials. Installing the plugin does not sign in to Noru.

- **OAuth:** run `/mcp auth noru` in an interactive session.
- **API key:** add the server to your private Copilot MCP configuration
  (`~/.copilot/mcp-config.json`), or use `/mcp add`, with the header
  `Authorization: Bearer <NORU_API_KEY>`. Keep that file out of git.

Do not paste OAuth tokens or API keys into assistant chat.

## First Prompt

```text
Help me become compliant with SOC 2 using Noru.
```
