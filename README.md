# compliance-assistant

Claude Code and Codex plugin that guides SOC 2, ISO 27001 and other framework work through Noru's MCP server. For Noru customers.

[![Plugin version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnoru-tech%2Fcompliance-assistant%2Fmain%2Fplugins%2Fcompliance-assistant%2F.claude-plugin%2Fplugin.json&query=%24.version&label=plugin)](./CHANGELOG.md)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/noru-tech/compliance-assistant/badge)](https://scorecard.dev/viewer/?uri=github.com/noru-tech/compliance-assistant)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](./LICENSE)
[![Codex Plugin](https://img.shields.io/badge/Codex-plugin-111827.svg)](./clients/codex.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-plugin-da7756.svg)](./clients/claude.md)

**Who it is for:** teams that already use Noru. It needs a Noru account and organization, and an
authenticated connection to Noru's MCP server; it does nothing on its own.

## Try it in three steps

1. **Install** the plugin in your client (commands below).
2. **Sign in to Noru.** The plugin already includes the `noru` MCP server, so you only authenticate
   it: run `/mcp` in Claude Code, choose `noru`, then **Authenticate**. In Codex, run
   `codex mcp login noru`. If you're not sure the connection works, ask *"Check my Noru connection"*.
3. **Ask** one of these:
   - *What should we do next for SOC 2?*
   - *Where are our biggest ISO 27001 gaps?*
   - *Are we ready for our audit? What would an auditor flag first?*

The assistant reads your live Noru data before it answers. It previews and asks for your yes
before changing anything in Noru.

## Which AI clients does it work with?

Claude Code, Codex, GitHub Copilot CLI, Gemini CLI and Cursor, plus any MCP client that can reach a
remote Streamable HTTP server. Install it in your client with the commands below.

### Claude Code

```text
/plugin marketplace add noru-tech/compliance-assistant
/plugin install compliance-assistant@compliance-assistant
```

Then run `/mcp` and authenticate `noru`. See [the Claude guide](./clients/claude.md) for API-key
and headless setup.

### Codex

```bash
codex plugin marketplace add noru-tech/compliance-assistant
codex plugin add compliance-assistant@compliance-assistant
```

Then run `codex mcp login noru`. See [the Codex guide](./clients/codex.md) for API-key setup.

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

- Two shared skills, following the [Agent Skills](https://agentskills.io/specification) format:
  - `compliance-assistant`: next steps, gap analysis, sufficiency advice, roadmaps, audit readiness,
    and policy, risk, vendor and privacy review, with safe, confirmed writes. Detailed workflows and
    the tool and scope reference live in `references/`.
  - `noru-setup`: connects and checks the Noru MCP server, explains missing scopes and inactive
    toolsets, and suggests first prompts. In Codex it is the plugin's onboarding skill.
- An eval suite (`plugins/compliance-assistant/evals/`) for `claude plugin eval`. The same cases
  serve as the review test cases for the OpenAI plugin directory.
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
| Wider read context | `read:vendors`, `read:personnel`, `read:assets`, `read:datamaps`, `read:users`, `read:internal-audits`, `read:external-audits`, `read:access-reviews`, `read:workflows`, `read:tickets` |
| Compliance tasks and roadmaps | `write:compliance` |
| Confirmed changes | Only the domain write scopes you need: `write:controls`, `write:policies`, `write:evidence`, `write:risks`, `write:vendors`, `write:personnel`, `write:assets`, `write:datamaps`, `write:internal-audits`, `write:external-audits`, `write:access-reviews`, `write:tickets` |
| Supplier risk (`tprm`) | `read:vendors`, plus `write:vendors` for changes; needs supplier risk management enabled |
| Trust center access | `read:trust-access`, plus `write:trust-access` to approve or revoke |
| Admin integrations | `read:webhooks`, `write:webhooks`, `write:workflows`, `read:signals` |

The full tool-to-scope map is in
[`references/tools.md`](./plugins/compliance-assistant/skills/compliance-assistant/references/tools.md).

### Toolsets

Noru groups its 383 tools into 22 toolsets, including `core`, `frameworks`, `controls`,
`policies`, `evidence`, `risks`, `vendors`, `tprm` (supplier risk), `personnel`, `datamaps`,
`internal-audits`, `external-audits`, `access-reviews`, `trust-access`, `tickets`, `compliance` and a
few admin sets. `core` is always on. A smaller tool list helps the assistant pick the right tool. To
limit the connection to the toolsets you use, add them to the server URL in your client's MCP
settings:

```text
https://api.noru.tech/v1/mcp?toolsets=controls,policies,evidence,risks
```

When a task needs a toolset that is not active, the assistant tells you which one to add.

See the client guides:

- [Codex](./clients/codex.md)
- [Claude Code and Claude Desktop](./clients/claude.md)
- [GitHub Copilot CLI](./clients/copilot.md)
- [Gemini CLI](./clients/gemini.md)
- [Cursor](./clients/cursor.md)
- [Generic MCP clients](./clients/generic-mcp.md)

## How does it decide what to do next?

It reads your organization's real Noru context first instead of guessing:

1. Check the connection: organization, granted scopes and active toolsets (`getMcpCapabilities`).
2. Read company context, enabled frameworks and the compliance overview.
3. For "is it sufficient?" or "do we need X?" questions, read Noru's guidance
   (`checkGuidanceRequirements`, `readGuidanceContent`). Keep policy (intent), evidence (observed
   operation) and saved answers (reported practice) apart.
4. For "what next?", read the framework plan and pending controls, and put blockers first.
5. Create tasks (`suggestComplianceTasks`) or a roadmap (`createCompliancePlan`) only when you ask
   for them.
6. Drill into controls, evidence, policies, risks, vendors or privacy records where they block the
   next step.

Before any change in Noru, the assistant says exactly what will change and previews the impact
(`previewChangeImpact`) where it applies. It changes nothing until you say yes.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| No `noru` tools, or "needs authentication" | Claude Code: `/mcp` → `noru` → **Authenticate**. Codex: `codex mcp login noru`. Copilot CLI or Gemini CLI: `/mcp auth noru`. |
| 401 or 403 after signing in | The token expired or was revoked. Sign in again. With an API key, check that it is still active in Noru → Developer settings. |
| The assistant reports a missing scope | Grant the scope named in the message to your OAuth app or API key in Noru, then reconnect. Use the table above to stay least-privilege. |
| The assistant says a toolset is inactive | Add the toolset to the `?toolsets=` list in the server URL, or remove the parameter to get every toolset your credential allows. |
| Wrong organization | You signed in to a different Noru organization. Sign out of `noru` in your client and sign in again. |
| Still stuck | Ask *"Check my Noru connection"*. The `noru-setup` skill reports what the connection can and cannot do. |

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
│   ├── submission.md              # Anthropic and OpenAI plugin directory checklist
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
│       ├── assets/                # Logo and composer icon
│       ├── evals/                 # claude plugin eval cases
│       └── skills/
│           ├── compliance-assistant/
│           │   ├── SKILL.md
│           │   ├── agents/openai.yaml   # Codex skill metadata
│           │   └── references/          # tools, scopes, workflows, safe actions
│           └── noru-setup/
│               ├── SKILL.md
│               └── agents/openai.yaml
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
- No telemetry. The installed plugin is two skills, MCP configuration, icons, eval cases and metadata, with
  no executable code; it talks only to the Noru MCP server your client is configured for.

## Security

Never commit API keys, tokens, customer identifiers, local MCP configs containing secrets, logs, or
captured customer output. This repo intentionally commits only placeholder configuration.

For private vulnerability reporting, see [SECURITY.md](./SECURITY.md).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

Maintained by [Noru](https://noru.tech), a continuous compliance platform.
