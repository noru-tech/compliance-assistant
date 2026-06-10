# Codex Setup

The Codex plugin metadata lives in `.codex-plugin/plugin.json`, and the shared skill lives in
`skills/compliance-assistant/SKILL.md`.

## Requirements

- Codex with plugin support.
- A Noru API key with the scopes needed for your workflow.
- `NORU_API_KEY` available only in your local environment or private MCP client configuration.

## Recommended Setup

Use the committed `.mcp.json` for the public endpoint, then configure bearer authentication in your
local Codex MCP settings:

```bash
export NORU_API_KEY="<your_noru_api_key>"
export NORU_API_URL="https://api.noru.tech/v1/mcp"
```

The server name is:

```text
noru
```

The MCP endpoint is:

```text
https://api.noru.tech/v1/mcp
```

Use the header:

```text
Authorization: Bearer <NORU_API_KEY>
```

Do not commit local Codex configuration files that contain the resolved bearer token.

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
