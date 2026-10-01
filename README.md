# compliance-assistant

Claude Code and Codex plugin that guides SOC 2, ISO 27001 and other framework work through Noru's MCP server. For Noru customers.

[![Plugin version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnoru-tech%2Fcompliance-assistant%2Fmain%2Fplugins%2Fcompliance-assistant%2F.claude-plugin%2Fplugin.json&query=%24.version&label=plugin)](./CHANGELOG.md)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/noru-tech/compliance-assistant/badge)](https://scorecard.dev/viewer/?uri=github.com/noru-tech/compliance-assistant)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](./LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827.svg)](./clients/codex.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-plugin-da7756.svg)](./clients/claude.md)

**Who it is for:** teams that already use Noru. It needs a Noru account and organization, and an
authenticated connection to Noru's MCP server; it does nothing on its own.

## Which AI clients does it work with?

Claude Code, Codex, GitHub Copilot CLI, Gemini CLI and Cursor, plus any MCP client that can reach a
remote Streamable HTTP server. Install it in your client with the commands below.

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

### GitHub Copilot CLI

Copilot CLI reads the same `.claude-plugin/marketplace.json`:

```bash
copilot plugin marketplace add noru-tech/compliance-assistant
copilot plugin install compliance-assistant@compliance-assistant
```

Then authenticate Noru MCP using [the Copilot CLI guide](./clients/copilot.md).

### Gemini CLI

```bash
gemini extensions install https://github.com/noru-tech/compliance-assistant
```

Then authenticate Noru MCP using [the Gemini CLI guide](./clients/gemini.md).

### Cursor and other MCP clients

The repository uses Cursor's plugin layout (`.cursor-plugin/`) but is not yet listed in the Cursor
Marketplace. Cursor and other MCP clients can connect to the same Noru MCP server; see
[Cursor](./clients/cursor.md) and [Generic MCP clients](./clients/generic-mcp.md).

### Is Noru's MCP server in the MCP Registry?

Yes, as `tech.noru/mcp`. Noru's remote MCP server is described for the official MCP Registry in
[`server.json`](./server.json). See [docs/mcp-registry.md](./docs/mcp-registry.md) for how it is
published.

## What does it do?

It guides your SOC 2, ISO 27001 or other framework work using your live Noru data.
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
- Claude Code marketplace metadata under `.claude-plugin/`, which GitHub Copilot CLI also reads.
- Cursor plugin and marketplace metadata under `.cursor-plugin/` and
  `plugins/compliance-assistant/.cursor-plugin/`.
- A Gemini CLI extension manifest, `gemini-extension.json`.
- An official MCP Registry entry for Noru's remote MCP server, `server.json`.
- Client setup guides for Codex, Claude Code/Desktop, GitHub Copilot CLI, Gemini CLI, Cursor, and
  generic MCP clients.
- A minimal configuration model: customers authenticate the Noru MCP connection with OAuth where
  their client supports it, or with `NORU_API_KEY` for manual/headless setup.

## How do I connect my AI assistant to Noru?

Connect your client to Noru's hosted MCP endpoint at `https://api.noru.tech/v1/mcp` and authenticate
with OAuth or a Noru API key.

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
- [GitHub Copilot CLI](./clients/copilot.md)
- [Gemini CLI](./clients/gemini.md)
- [Cursor](./clients/cursor.md)
- [Generic MCP clients](./clients/generic-mcp.md)

## How does it decide what to do next?

It reads your organization's real Noru context first instead of guessing:

1. Read organization context.
2. Read enabled frameworks and framework compliance overview.
3. Use the `assessFrameworkGaps` prompt for posture framing.
4. Use `suggestComplianceTasks` for prioritized next work.
5. Use `createCompliancePlan` only when the user asks for a roadmap or timeline.
6. Drill into controls, evidence, policies, and risks where they block the next compliance step.

External clients must ask for explicit user confirmation before write-like actions such as drafting
policies, changing control status, creating or linking evidence, or updating risks.

## What it is not

- Not a standalone compliance tool. It holds no compliance data of its own; everything comes from
  your Noru organization.
- Not usable without a Noru organization and an authenticated `noru` MCP connection.
- Not a credential store. It does not store secrets or perform sign-in; the MCP host or client
  manages authentication.
- Not a way around Noru permissions. It reads and writes only through the MCP server's tools, limited
  to the scopes granted to your OAuth grant or API key.
- Not autonomous. Write-like actions (policy drafting, control status changes, evidence and risk
  updates) require your explicit confirmation first.

## Repository Layout

```text
compliance-assistant/
├── .agents/
│   └── plugins/
│       └── marketplace.json       # Codex marketplace
├── .claude-plugin/
│   └── marketplace.json           # Claude Code marketplace (also read by Copilot CLI)
├── .cursor-plugin/
│   └── marketplace.json           # Cursor marketplace
├── .github/                       # Issue forms, PR template, Dependabot, CI and publish workflows
├── clients/
│   ├── codex.md
│   ├── claude.md
│   ├── copilot.md
│   ├── gemini.md
│   ├── cursor.md
│   └── generic-mcp.md
├── docs/
│   ├── mcp-registry.md            # Publishing server.json to the MCP Registry
│   └── openssf-best-practices.md  # Prepared OpenSSF Best Practices badge answers
├── plugins/
│   └── compliance-assistant/
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── .cursor-plugin/
│       │   └── plugin.json
│       ├── .mcp.json              # Claude Code, Codex, Copilot CLI
│       ├── mcp.json               # Cursor
│       └── skills/
│           └── compliance-assistant/
│               └── SKILL.md
├── scripts/
│   └── check_repo.py              # Stdlib-only repository checks
├── gemini-extension.json          # Gemini CLI extension
├── server.json                    # Official MCP Registry entry (tech.noru/mcp)
├── llms.txt                       # Summary and install paths for AI agents (llmstxt.org format)
├── .env.example
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── CHANGELOG.md
```

## Related

[`noru-tech/noru-grc-engineering`](https://github.com/noru-tech/noru-grc-engineering) is the other
half of the same job, over the same MCP server. This repository is the **conversation**: what to do
next, which controls block which, what the gaps are, what a roadmap looks like. That one is the
**hands-on work in a repository** — inventorying the AI systems a codebase contains, building a
privacy data map from its schemas, scanning infrastructure configuration, pushing local evidence,
assembling an audit pack — each landing in Noru with a `file:line` citation and a named owner.

They are deliberately separate and install side by side. This one is useful with no repository at
all, in any MCP client; those need a git work tree, write `.noru/*.yml` into it, and run in CI on a
pull request.

## Does it collect data or run code?

No. It has no telemetry, the installed plugin contains no executable code, and it talks only to the
Noru MCP server your client is configured for.

- MIT licensed; see [LICENSE](./LICENSE).
- Report vulnerabilities privately; see [SECURITY.md](./SECURITY.md).
- No telemetry. The installed plugin is a skill, MCP configuration and metadata with no executable
  code; it talks only to the Noru MCP server your client is configured for.

## Security

Never commit API keys, tokens, customer identifiers, local MCP configs containing secrets, logs, or
captured customer output. This repo intentionally commits only placeholder configuration.

For private vulnerability reporting, see [SECURITY.md](./SECURITY.md).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

Maintained by [Noru](https://noru.tech), a continuous compliance platform.
