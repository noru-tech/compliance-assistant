# Gemini CLI Setup

This repository is also a Gemini CLI extension. The root
[`gemini-extension.json`](../gemini-extension.json) does two things:

- registers the Noru MCP server as `noru`, using streamable HTTP at `https://api.noru.tech/v1/mcp`;
- loads the shared skill guidance
  (`plugins/compliance-assistant/skills/compliance-assistant/SKILL.md`) as the extension's
  context file.

Format source: `google-gemini/gemini-cli` `docs/extensions/reference.md`,
`docs/extensions/releasing.md` and `docs/tools/mcp-server.md`, at commit
`c6bccb7ecbf6d8368d995455dd725ed34466faad`.

## Install

```bash
gemini extensions install https://github.com/noru-tech/compliance-assistant
```

To pin a tag, add `--ref v0.1.1`. Restart Gemini CLI after you install or update. To update later:

```bash
gemini extensions update compliance-assistant
```

## Authentication

Installing the extension does not sign in to Noru or store credentials.

- **OAuth:** the extension does not set an `Authorization` header, so Gemini CLI can discover Noru's
  OAuth configuration on its own. Run `/mcp auth noru` in Gemini CLI to sign in.
- **API key:** in your user `~/.gemini/settings.json`, define a server with the same name `noru`.
  A server in `settings.json` takes precedence over the extension's server of the same name. Keep
  the file out of git.

```json
{
  "mcpServers": {
    "noru": {
      "httpUrl": "https://api.noru.tech/v1/mcp",
      "headers": {
        "Authorization": "Bearer <NORU_API_KEY>"
      }
    }
  }
}
```

Do not paste OAuth tokens or API keys into assistant chat.

## First Prompt

```text
Help me become compliant with SOC 2 using Noru.
```
