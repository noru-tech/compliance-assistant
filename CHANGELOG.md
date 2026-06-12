# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Clarified that Noru MCP authentication is managed by each MCP host or client.
- Documented OAuth as the preferred option where supported, with API keys for manual/headless setup.

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

[Unreleased]: https://github.com/noru-tech/compliance-assistant/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/noru-tech/compliance-assistant/releases/tag/v0.1.0
