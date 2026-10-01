# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `llms.txt` at the repository root, following the llmstxt.org format: the canonical description,
  who it is for, install commands for every supported client, the MCP endpoint and links to the
  client guides, `docs/mcp-registry.md`, `SECURITY.md` and the README's "What it is not".
- `docs/openssf-best-practices.md`: prepared answers for the OpenSSF Best Practices "passing" criteria,
  each Met, Unmet or N/A with evidence. One MUST (`test_policy`) is still Unmet.
- `server.json`: official MCP Registry entry for Noru's remote MCP server (`tech.noru/mcp`,
  streamable HTTP at `https://api.noru.tech/v1/mcp`, optional API-key bearer header for clients
  without OAuth). It is published by a manual-only `publish-mcp-registry` workflow that uses DNS
  authentication for `noru.tech` and a pinned, checksum-verified `mcp-publisher`. One-time setup is
  in `docs/mcp-registry.md`.
- Gemini CLI extension manifest (`gemini-extension.json`). It registers the Noru MCP server and
  loads the skill guidance as context. Guide: `clients/gemini.md`.
- Cursor plugin metadata (`.cursor-plugin/marketplace.json`,
  `plugins/compliance-assistant/.cursor-plugin/plugin.json` and `plugins/compliance-assistant/mcp.json`)
  following Cursor's published plugin schemas.
- GitHub Copilot CLI install instructions (`clients/copilot.md`). Copilot CLI reads the existing
  `.claude-plugin/marketplace.json`.
- `scripts/check_repo.py` checks the new manifests and fails if any manifest's version differs from
  the plugin version.

- CodeQL static analysis of the Python and workflow code on every pull request, on main and weekly.
- OpenSSF Scorecard workflow with SARIF upload and pinned action SHAs.
- Dependabot configuration for GitHub Actions.
- Issue forms (bug report, feature request), pull request template and CODEOWNERS.

### Changed

- README: several headings are now the questions people ask ("Which AI clients does it work with?",
  "How do I connect my AI assistant to Noru?", "What does it do?", "How does it decide what to do
  next?", "Does it collect data or run code?"), each answered in its first sentence. Content and order
  are unchanged.
- README: the version badge reads the plugin's own version from `plugin.json`; the repository
  publishes tags but no GitHub Releases, so the release badge showed "no releases".
- README now opens with the canonical description, a badge row, a "Who it is for" line, install
  commands near the top, and "What it is not" and "Trust" sections.
- Plugin and marketplace manifest descriptions use the canonical description.
- SECURITY.md links GitHub Private Vulnerability Reporting for this repository.

## [0.1.1] - 2026-08-28

### Changed

- Clarified that Noru MCP authentication is managed by each MCP host or client.
- Documented OAuth as the preferred option where supported, with API keys for manual/headless setup.
- Linked to noru-grc-engineering and documented the production MCP endpoint.

## [0.1.0] - 2026-06-10

### Added

- Initial public plugin scaffold for `compliance-assistant`.
- Codex marketplace metadata under `.agents/plugins/marketplace.json`.
- Installable plugin payload under `plugins/compliance-assistant/`.
- Claude Code plugin and marketplace metadata.
- Shared `compliance-assistant` skill for guided Noru compliance workflows.
- Client setup docs for Codex, Claude, Cursor, and generic MCP clients.
- Public repo hygiene files and placeholder-only environment example.
- `scripts/check_repo.py` for stdlib-only repository, marketplace, plugin, and secret-hygiene checks.

[Unreleased]: https://github.com/noru-tech/compliance-assistant/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/noru-tech/compliance-assistant/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/noru-tech/compliance-assistant/releases/tag/v0.1.0
