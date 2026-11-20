---
name: noru-setup
description: Connects and checks the Noru MCP server for the compliance assistant. Use when the user is setting up the Noru plugin, when no noru tools are available, when a Noru call fails with 401, 403 or a missing-scope error, when the wrong organization appears, or when the user asks what the Noru connection can do.
license: MIT
metadata:
  version: "0.2.0"
---

# Noru setup and connection check

Get the user from "plugin installed" to a working, least-privilege Noru connection. Then hand over
to the `compliance-assistant` skill.

Never ask for, accept or repeat an OAuth token or API key in chat. If the user pastes one, do not
use it, and do not quote it back, not even partly or in code formatting. Call it "the key you
pasted", tell them to revoke it in Noru and create a new one, and point them to the sign-in step
below.

## 1. Is the server connected?

Try `noru:getMcpCapabilities`.

- **It works**: go to step 2.
- **No `noru` tools exist, or the call returns 401 or 403**: the plugin ships the `noru` server
  (`https://api.noru.tech/v1/mcp`), so the user only needs to sign in. Give the step for their client:

| Client | Sign in |
| --- | --- |
| Claude Code | Run `/mcp`, select `noru` (shown as `plugin:compliance-assistant:noru`), choose **Authenticate**, and finish the browser sign-in. |
| Codex | Run `codex mcp login noru` in a terminal, then restart the session. |
| Copilot CLI or Gemini CLI | Run `/mcp auth noru`. |
| Cursor | Sign in to the `noru` server from Cursor's MCP settings. |

Headless or CI use needs an API key instead of OAuth: the user creates a Noru API key in Noru →
Developer settings and adds it to their **private** client config as
`Authorization: Bearer <NORU_API_KEY>`. The client guides in the plugin repository show the exact
config for each client.

After sign-in, call `noru:getMcpCapabilities` again.

## 2. Report what the connection can do

From the `getMcpCapabilities` result, tell the user in a few lines:

- **Organization**: the name. If it is not the one they expected, they signed in to the wrong Noru
  organization and should reconnect.
- **Access**: read-only, or read and write, and which domains (frameworks, controls, policies,
  evidence, risks, vendors, privacy, and so on).
- **Gaps**: missing scopes, and inactive toolsets the user is likely to need. Use
  [../compliance-assistant/references/scopes-and-toolsets.md](../compliance-assistant/references/scopes-and-toolsets.md)
  to name the smallest addition.

Keep it short. Do not dump the full tool list.

## 3. Suggest first prompts

Pick three that fit their enabled frameworks (`noru:getOrganizationFrameworks`), for example:

- "What should we do next for SOC 2?"
- "Where are our biggest ISO 27001 gaps?"
- "Are we ready for our audit? What would an auditor flag first?"

Then continue with the `compliance-assistant` skill.
