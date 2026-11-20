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

The plugin includes the `noru` MCP server (`https://api.noru.tech/v1/mcp`). Installing doesn't sign
you in to Noru or store any credentials.

### OAuth (recommended)

```bash
codex mcp login noru
```

Finish the sign-in in your browser, then start a new Codex session. When you first use the plugin,
Codex runs its onboarding skill, `noru-setup`. You can also ask:

```text
Use $noru-setup to check my Noru connection.
```

### API key (headless or CI)

Use this only when OAuth isn't possible. In your private `~/.codex/config.toml`, turn off the
plugin's server and add your own that sends the key from an environment variable:

```toml
[plugins."compliance-assistant".mcp_servers.noru]
enabled = false

[mcp_servers.noru]
url = "https://api.noru.tech/v1/mcp"
bearer_token_env_var = "NORU_API_KEY"
```

```bash
export NORU_API_KEY="<your_noru_api_key>"
```

Don't paste OAuth tokens or API keys into assistant chat. Don't commit local Codex configuration
files that contain resolved credentials.

## First prompts

The plugin card offers these as starter prompts:

```text
What should we do next for SOC 2?
Where are our biggest ISO 27001 gaps?
Are we ready for our audit? What would an auditor flag first?
```

The assistant checks the connection and reads your organization, enabled frameworks and compliance
overview before it recommends an order of work.

## Scopes

For guidance-only use, start with read scopes:

```text
read:organization read:frameworks read:controls read:policies read:evidence read:risks
```

Add `write:compliance` when you want prioritized task suggestions or compliance roadmaps. Add domain
write scopes only when you want the assistant to perform confirmed actions. The full map is in
[the scope and toolset reference](../plugins/compliance-assistant/skills/compliance-assistant/references/scopes-and-toolsets.md).
