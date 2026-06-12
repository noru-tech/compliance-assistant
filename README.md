# compliance-assistant

> Guide Noru customers through framework compliance work using Noru's remote MCP server.

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](./LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827.svg)](./clients/codex.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-plugin-da7756.svg)](./clients/claude.md)

`compliance-assistant` is an open source assistant package for Noru customers. It packages a shared
agent skill and client setup docs for working with Noru over MCP, with installable metadata for
Codex and Claude Code.

The assistant helps answer questions like:

> Help me become compliant with SOC 2 using Noru.

It connects to Noru's hosted MCP endpoint, reads your organization's compliance context, and guides
the next best sequence of controls, policies, evidence, risks, and roadmap work.

## What You Get

- A shared `compliance-assistant` skill for compliance sequencing and safe Noru MCP usage.
- Codex marketplace metadata under `.agents/plugins/marketplace.json`.
- Codex and Claude Code plugin metadata under `plugins/compliance-assistant/`.
- Claude Code marketplace metadata under `.claude-plugin/`.
- Client setup guides for Codex, Claude Code/Desktop, Cursor, and generic MCP clients.
- A minimal configuration model: customers authenticate the Noru MCP connection with OAuth where
  their client supports it, or with `NORU_API_KEY` for manual/headless setup.

## Configuration

The public package connects to Noru's hosted MCP endpoint at `https://api.noru.tech/v1/mcp`.

The plugin does not store secrets or perform sign-in itself. Authentication is managed by the MCP
host or client. If that client already has an authenticated `noru` MCP connection, this plugin can
use it. MCP connections are local to the host: a connection configured in ChatGPT does not
automatically authenticate Codex, Claude, Cursor, or another client.

For a new connection, use one authentication path:

- OAuth, when your MCP client supports OAuth for remote MCP servers.
- A Noru API key, when your client needs manual bearer-token or headless configuration.

For API-key setup, create a Noru API key in Noru Developer settings, then expose it only to your
local MCP client:

```bash
export NORU_API_KEY="<your_noru_api_key>"
```

Both OAuth and API-key setup result in a bearer credential sent to Noru MCP. Do not paste
credentials into assistant chat or commit local auth configuration.

Use least-privilege scopes for the job:

| Capability | Scopes |
| --- | --- |
| Core read-only guidance | `read:organization`, `read:frameworks`, `read:controls`, `read:policies`, `read:evidence`, `read:risks` |
| Optional read context | `read:users`, `read:vendors`, `read:assets`, `read:personnel`, `read:datamaps` |
| Compliance tasks and roadmaps | `write:compliance` |
| Optional execution actions | Relevant domain write scopes such as `write:policies`, `write:controls`, `write:evidence`, `write:risks` |

See the client guides:

- [Codex](./clients/codex.md)
- [Claude Code and Claude Desktop](./clients/claude.md)
- [Cursor](./clients/cursor.md)
- [Generic MCP clients](./clients/generic-mcp.md)

## How It Works

The skill starts by discovering real Noru context instead of guessing:

1. Read organization context.
2. Read enabled frameworks and framework compliance overview.
3. Use the `assessFrameworkGaps` prompt for posture framing.
4. Use `suggestComplianceTasks` for prioritized next work.
5. Use `createCompliancePlan` only when the user asks for a roadmap or timeline.
6. Drill into controls, evidence, policies, and risks where they block the next compliance step.

External clients must ask for explicit user confirmation before write-like actions such as drafting
policies, changing control status, creating or linking evidence, or updating risks.

## Repository Layout

```text
compliance-assistant/
├── .agents/
│   └── plugins/
│       └── marketplace.json       # Codex marketplace
├── .claude-plugin/
│   └── marketplace.json           # Claude Code marketplace
├── clients/
│   ├── codex.md
│   ├── claude.md
│   ├── cursor.md
│   └── generic-mcp.md
├── plugins/
│   └── compliance-assistant/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── .mcp.json
│       └── skills/
│           └── compliance-assistant/
│               └── SKILL.md
├── .env.example
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── CHANGELOG.md
```

## Install

### Claude Code

```text
/plugin marketplace add noru-tech/compliance-assistant
/plugin install compliance-assistant@compliance-assistant
```

Then configure Noru MCP using [the Claude guide](./clients/claude.md).

### Codex

```bash
codex plugin marketplace add noru-tech/compliance-assistant
codex plugin add compliance-assistant@compliance-assistant
```

Then configure Noru MCP using [the Codex guide](./clients/codex.md).

## Security

Never commit API keys, tokens, customer identifiers, local MCP configs containing secrets, logs, or
captured customer output. This repo intentionally commits only placeholder configuration.

For private vulnerability reporting, see [SECURITY.md](./SECURITY.md).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
