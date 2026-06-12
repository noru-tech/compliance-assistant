# Codex Setup

The Codex marketplace metadata lives in `.agents/plugins/marketplace.json`. The installable plugin
payload lives in `plugins/compliance-assistant/`.

## Requirements

- Codex with plugin support.
- An authenticated Noru MCP connection in Codex, using OAuth where supported or a Noru API key for
  manual/headless setup.

## Recommended Setup

Install from the repo marketplace:

```bash
codex plugin marketplace add noru-tech/compliance-assistant
codex plugin add compliance-assistant@compliance-assistant
```

For local branch testing, add the local checkout instead:

```bash
codex plugin marketplace add <path-to-compliance-assistant-checkout>
codex plugin add compliance-assistant@compliance-assistant
```

## Authentication

Plugin installation does not sign in to Noru or store credentials. Codex manages MCP authentication
for the `noru` server outside the plugin payload. If Codex already has an authenticated `noru`
connection, the installed skill can use it.

For a new connection, use OAuth if your Codex build supports OAuth for remote MCP servers. Otherwise,
configure bearer authentication in your local Codex MCP settings with a Noru API key:

```bash
export NORU_API_KEY="<your_noru_api_key>"
```

The server name is:

```text
noru
```

The MCP endpoint is:

```text
https://api.noru.tech/v1/mcp
```

API-key setup uses the header:

```text
Authorization: Bearer <NORU_API_KEY>
```

Do not paste OAuth tokens or API keys into assistant chat. Do not commit local Codex configuration
files that contain resolved credentials.

## First Prompt

```text
Help me become compliant with SOC 2 using Noru.
```

The assistant should discover organization context, enabled frameworks, and framework compliance
overview before recommending an execution order.

## Scopes

For guidance-only use, start with read scopes:

```text
read:organization read:frameworks read:controls read:policies read:evidence read:risks
```

Add `write:compliance` when you want prioritized task suggestions or compliance roadmaps. Add domain
write scopes only when you want the assistant to perform confirmed actions.
