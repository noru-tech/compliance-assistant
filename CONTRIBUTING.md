# Contributing to compliance-assistant

Thanks for improving `compliance-assistant`. This repo is intentionally small and public: plugin
metadata, two shared skills, an eval suite, client docs, and security-focused setup examples.

## Ground Rules

- Be respectful — see [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
- Keep the plugin atomic: runtime code must use only the Python standard library, with no network
  access and no third-party install step. The Python standard library is considered atomic for this
  repo; stdlib-only scripts do not require dependency management. PyYAML may be used
  opportunistically, but a stdlib fallback must remain.
- Never commit Noru API keys, OAuth tokens, bearer tokens, customer identifiers, generated customer
  configs, logs, or captured customer output.
- Use placeholders such as `<NORU_API_KEY>` and `${NORU_API_KEY}` in examples.
- Keep examples oriented around least-privilege scopes.
- Update `CHANGELOG.md` for user-visible changes.

## Project Layout

- `.agents/plugins/marketplace.json` contains the Codex marketplace entry.
- `.claude-plugin/marketplace.json` contains the Claude Code marketplace entry; GitHub Copilot CLI
  reads it too.
- `.cursor-plugin/marketplace.json` and `plugins/compliance-assistant/.cursor-plugin/plugin.json`
  contain the Cursor plugin metadata.
- `gemini-extension.json` is the Gemini CLI extension manifest.
- `server.json` is the official MCP Registry entry for Noru's remote MCP server; see
  `docs/mcp-registry.md`.
- When you bump the plugin version, update every manifest that carries it. `scripts/check_repo.py`
  fails if they disagree.
- `plugins/compliance-assistant/` contains the installable plugin payload.
- `plugins/compliance-assistant/skills/compliance-assistant/SKILL.md` contains the shared assistant
  workflow. Detail lives in its `references/`; keep `SKILL.md` short.
- `plugins/compliance-assistant/skills/compliance-assistant/references/tools.md` is the snapshot of
  Noru MCP tools and scopes. When the server adds or renames tools, regenerate it from a Noru
  checkout of the deployed commit, with dependencies installed:
  `bun scripts/refresh-tools-reference.ts <path-to-noru>`. The checker fails if a skill mentions a
  `noru:tool` that is not listed there.
- `plugins/compliance-assistant/skills/noru-setup/` is the onboarding and connection-check skill.
- Skill frontmatter follows the Agent Skills spec: only `name`, `description`, `license`,
  `compatibility`, `metadata` and `allowed-tools`. The version goes in `metadata.version`.
- Each skill has `agents/openai.yaml` with its Codex display metadata.
- Anthropic's plugin directory accepts only Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO
  files in the plugin folder from unverified organizations. Never add `.svg` files or scripts there;
  the checker fails if you do.
- `plugins/compliance-assistant/evals/` holds `claude plugin eval` cases.
- `clients/` contains setup docs for MCP clients.

## Development & Testing

There is no build step. Verify changes with the bundled stdlib-only checker:

```bash
python3 scripts/check_repo.py
```

This validates the Codex marketplace, installable plugin metadata, Claude and Cursor marketplace
metadata, the Gemini extension manifest, the MCP Registry `server.json`, MCP config, skill
frontmatter and links, placeholder environment config, and basic secret hygiene. CI runs it on every
pull request (`.github/workflows/check.yml`), together with Claude Code's own validator:

```bash
bunx @anthropic-ai/claude-code@2.1.329 plugin validate --strict plugins/compliance-assistant
bunx @anthropic-ai/claude-code@2.1.329 plugin validate --strict .claude-plugin/marketplace.json
```

### Evals

The eval suite runs offline: `plugins/compliance-assistant/evals/mocks/noru/` holds fixed responses
for a fictional organization, so no Noru sign-in is needed and no run can change a real workspace.
It costs model usage (about $1 for one run of every case), so it is not part of CI. Run it after
changing a skill:

```bash
cd plugins/compliance-assistant
bunx @anthropic-ai/claude-code@2.1.329 plugin eval . --runs 1 --ablation none --no-publish
```

When a case starts using a Noru tool that has no mock, add `evals/mocks/noru/<tool>.md`. A tool with
no mock is not available in the run.

Results go to `evals/results/`, which git ignores.

**Test policy:** a pull request that adds a manifest, a manifest field or any other behaviour the
checker can verify must add the matching check to `scripts/check_repo.py` in the same pull request.

For local Codex installability, run:

```bash
tmpdir="$(mktemp -d)"
CODEX_HOME="$tmpdir" codex plugin marketplace add <path-to-this-repo>
CODEX_HOME="$tmpdir" codex plugin list --marketplace compliance-assistant
CODEX_HOME="$tmpdir" codex plugin add compliance-assistant@compliance-assistant
```

The temporary `CODEX_HOME` keeps the check out of your real Codex configuration.

## Verification

Before opening a pull request:

```bash
python3 scripts/check_repo.py
git diff --check
```

If you have the Codex plugin-creator validation script installed, also run it against the repository
plugin root:

```bash
python3 <plugin-creator-skill>/scripts/validate_plugin.py plugins/compliance-assistant
```

Also inspect staged content for secrets:

```bash
git grep -n "noru_[A-Za-z0-9]" -- .
git grep -n "Bearer [A-Za-z0-9]" -- .
```

Those commands should find no real secrets. Placeholder strings such as `Bearer <NORU_API_KEY>` or
`Bearer <access_token_or_api_key>` are acceptable in documentation.

## Pull Requests

1. Create a focused branch from `main`.
2. Make scoped changes.
3. Run the verification steps above.
4. Open a PR describing the behavior change, testing, and any security implications.

By contributing, you agree that your code and documentation contributions are licensed under this
project's MIT license.
