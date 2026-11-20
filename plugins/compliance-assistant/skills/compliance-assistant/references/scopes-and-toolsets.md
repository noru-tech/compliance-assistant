# Scopes and toolsets

A Noru MCP tool is available only when both of these hold:

1. **Scope**: the OAuth grant or API key includes the tool's scope (see [tools.md](tools.md)).
2. **Toolset**: the tool's toolset is active on this connection.

`noru:getMcpCapabilities` reports the granted scopes, the tools listed for this connection, and
every toolset the credential could use, marked active or inactive.

## Least-privilege bundles

Recommend the smallest bundle that covers what the user asked for.

| Use | Scopes |
| --- | --- |
| Guidance only (read) | `read:organization read:frameworks read:controls read:policies read:evidence read:risks` |
| Wider read context | add `read:vendors read:personnel read:assets read:datamaps read:users read:internal-audits read:workflows` |
| Tasks and roadmaps | add `write:compliance` |
| Confirmed changes | add only the domain write scopes needed: `write:controls`, `write:policies`, `write:evidence`, `write:risks`, `write:vendors`, `write:personnel`, `write:assets`, `write:datamaps`, `write:internal-audits` |
| Admin integrations | `read:webhooks write:webhooks read:workflows write:workflows read:signals` |

When a scope is missing, name the capability that is unavailable and the scope that would enable it.
Then carry on with what the granted scopes allow. Granting scopes happens in Noru, never in chat.

## Toolsets

Toolsets keep the tool list small so the assistant picks the right tool. `core` is always on. It
holds the organization, connection capabilities, the compliance overview and the guidance tools.

| Toolset | Covers |
| --- | --- |
| `core` | Organization, capabilities, compliance overview, guidance |
| `users` | The signed-in user and their own training |
| `frameworks` | Available and enabled frameworks, and the plan for each |
| `controls` | Controls, status, owners, context, implementation briefs, SoA |
| `risks` | Risk register, treatments, control mappings, security findings |
| `evidence` | Evidence records and their links to controls |
| `policies` | Policies, content, versions, approvers, control mappings |
| `vendors` | Vendors, contacts, owners, status, vendor evidence |
| `personnel` | People, training plans and campaigns, policy acknowledgements |
| `assets` | Asset inventory |
| `datamaps` | Privacy: data map, RoPA, assessments, data sources, AI register |
| `ai-inventory` | Ingesting and reviewing an AI inventory |
| `internal-audits` | Internal audits, findings and reports |
| `webhooks` | Webhook endpoints and deliveries (admin) |
| `workflows` | Workflows, runs and tasks waiting on people |
| `signals` | Signal types workflows can react to |
| `compliance` | Compliance plans, suggested tasks, plan steps, workstream leads |

When a task needs a tool from an inactive toolset, tell the user to add that toolset to the server
URL as a comma-separated `toolsets` query parameter, for example:

```text
https://api.noru.tech/v1/mcp?toolsets=controls,policies,evidence,risks
```

The user changes this in their client's MCP settings (for Claude Code, a user-level `noru` server
entry; for Codex, `~/.codex/config.toml`) and then reconnects.
