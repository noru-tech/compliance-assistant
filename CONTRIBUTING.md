# Contributing to compliance-assistant

Thanks for improving `compliance-assistant`. This repo is intentionally small and public: plugin
metadata, one shared skill, client docs, and security-focused setup examples.

## Ground Rules

- Be respectful — see [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
- Keep the plugin atomic: runtime code must use only the Python standard library, with no network
  access and no third-party install step. The Python standard library is considered atomic for this
  repo; stdlib-only scripts do not require dependency management. PyYAML may be used
  opportunistically, but a stdlib fallback must remain.
- Never commit Noru API keys, bearer tokens, customer identifiers, generated customer configs, logs,
  or captured customer output.
- Use placeholders such as `<NORU_API_KEY>` and `${NORU_API_KEY}` in examples.
- Keep examples oriented around least-privilege scopes.
- Update `CHANGELOG.md` for user-visible changes.

## Project Layout

- `.agents/plugins/marketplace.json` contains the Codex marketplace entry.
- `.claude-plugin/marketplace.json` contains the Claude Code marketplace entry.
- `plugins/compliance-assistant/` contains the installable plugin payload.
- `plugins/compliance-assistant/skills/compliance-assistant/SKILL.md` contains the shared assistant workflow.
- `clients/` contains setup docs for MCP clients.

## Development & Testing

There is no build step. Verify changes with the bundled stdlib-only checker:

```bash
python3 scripts/check_repo.py
```

This validates the Codex marketplace, installable plugin metadata, Claude marketplace metadata, MCP
config, skill frontmatter, placeholder environment config, and basic secret hygiene.

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

Those commands should find no real secrets. Placeholder strings such as `Bearer <NORU_API_KEY>` are
acceptable in documentation.

## Pull Requests

1. Create a focused branch from `main`.
2. Make scoped changes.
3. Run the verification steps above.
4. Open a PR describing the behavior change, testing, and any security implications.

By contributing, you agree that your code and documentation contributions are licensed under this
project's MIT license.
