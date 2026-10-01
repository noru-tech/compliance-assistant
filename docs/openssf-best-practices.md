# OpenSSF Best Practices: prepared answers

These are draft answers for the "passing" level of the
[OpenSSF Best Practices badge](https://www.bestpractices.dev/en/criteria/0). The project has not
been submitted yet. A maintainer should check each answer against the current repository before
copying it into the form.

Source: `coreinfrastructure/best-practices-badge` at commit
`e1b85623fd6ccad3283943db5957f3130e6bb84b`, `criteria/criteria.yml` (level `0`) and
`config/locales/en.yml`. Criteria marked `future` or `obsolete` there are left out.

## How to read these answers

This repository ships an agent skill (Markdown), plugin and marketplace manifests (JSON) and client
setup docs. The installed plugin contains no executable code. The only code in the repository is
`scripts/check_repo.py`, a standard-library check that maintainers run at development time, plus
GitHub Actions workflows. Many criteria about builds, tests, warnings and cryptography were written
for compiled or executable software. They apply weakly here, and the answers say so.

- **Met**: true today, with evidence.
- **Unmet**: not true today. The answer says what would change it.
- **N/A**: the criterion allows N/A and does not apply to this kind of project.

Repository: <https://github.com/noru-tech/compliance-assistant>. Evidence links point at `main`.

## Summary

Against the 67 current passing criteria: **47 Met, 4 Unmet, 16 N/A**. Every MUST is Met or N/A;
the remaining Unmet criteria are SHOULD or SUGGESTED.

| Unmet | Level | What would change it |
| --- | --- | --- |
| `test_invocation` | SHOULD | Make the checks runnable with `python3 -m unittest`, or accept that a stdlib script has no standard runner. |
| `test_most` | SUGGESTED | The checks cover manifests and secret hygiene, not the skill's prose instructions. |
| `dynamic_analysis` | SUGGESTED | No runtime code to analyse. N/A is not allowed for this criterion. |
| `dynamic_analysis_enable_assertions` | SUGGESTED | As above. |

## Basics

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `description_good` | MUST | Met | The README's first line: "Claude Code and Codex plugin that guides SOC 2, ISO 27001 and other framework work through Noru's MCP server. For Noru customers." <https://github.com/noru-tech/compliance-assistant#readme> |
| `interact` | MUST | Met | Obtain: [install commands](https://github.com/noru-tech/compliance-assistant/blob/main/README.md#which-ai-clients-does-it-work-with). Feedback: [issue forms](https://github.com/noru-tech/compliance-assistant/issues/new/choose). Contribute: [CONTRIBUTING.md](https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md). |
| `contribution` | MUST | Met | Pull requests from a focused branch, with the checks to run first: <https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md#pull-requests> |
| `contribution_requirements` | SHOULD | Met | Ground rules (stdlib only, no secrets, placeholders, least-privilege scopes, changelog) and required checks: <https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md#ground-rules> |
| `floss_license` | MUST | Met | MIT. <https://github.com/noru-tech/compliance-assistant/blob/main/LICENSE> |
| `floss_license_osi` | SUGGESTED | Met | MIT is OSI-approved. |
| `license_location` | MUST | Met | `LICENSE` at the repository root: <https://github.com/noru-tech/compliance-assistant/blob/main/LICENSE> |
| `documentation_basics` | MUST | Met | README (what it is, install, configuration, limits) and one guide per client in `clients/`: <https://github.com/noru-tech/compliance-assistant/blob/main/README.md> |
| `documentation_interface` | MUST | Met | The external interface is the plugin payload: the skill's workflow ([SKILL.md](https://github.com/noru-tech/compliance-assistant/blob/main/plugins/compliance-assistant/skills/compliance-assistant/SKILL.md)), the MCP server configuration and its auth inputs ([README](https://github.com/noru-tech/compliance-assistant/blob/main/README.md#how-do-i-connect-my-ai-assistant-to-noru), [generic MCP guide](https://github.com/noru-tech/compliance-assistant/blob/main/clients/generic-mcp.md)), and the registry entry ([docs/mcp-registry.md](https://github.com/noru-tech/compliance-assistant/blob/main/docs/mcp-registry.md)). The MCP tools themselves belong to Noru's hosted server, not this project. |
| `sites_https` | MUST | Met | The repository, install sources (GitHub) and the MCP endpoint `https://api.noru.tech/v1/mcp` are HTTPS only. |
| `discussion` | MUST | Met | GitHub issues and pull requests: searchable, addressable by URL, open to anyone with a free account, no proprietary client needed. <https://github.com/noru-tech/compliance-assistant/issues> |
| `english` | SHOULD | Met | All documentation is in English, and issues are accepted in English. |
| `maintained` | MUST | Met | Regular commits and merged pull requests, most recently in October 2026: <https://github.com/noru-tech/compliance-assistant/commits/main> |

## Change control

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `repo_public` | MUST | Met | <https://github.com/noru-tech/compliance-assistant> |
| `repo_track` | MUST | Met | Git records the author, date and content of every change: <https://github.com/noru-tech/compliance-assistant/commits/main> |
| `repo_interim` | MUST | Met | Work lands through pull requests between releases (for example #6 to #9 after 0.1.1): <https://github.com/noru-tech/compliance-assistant/pulls?q=is%3Apr> |
| `repo_distributed` | SUGGESTED | Met | Git. |
| `version_unique` | MUST | Met | Each release has a version in every manifest, and `scripts/check_repo.py` fails if they disagree: <https://github.com/noru-tech/compliance-assistant/blob/main/plugins/compliance-assistant/.claude-plugin/plugin.json> |
| `version_semver` | SUGGESTED | Met | SemVer, stated in the changelog and enforced by the checker's version pattern: <https://github.com/noru-tech/compliance-assistant/blob/main/CHANGELOG.md> |
| `version_tags` | SUGGESTED | Met | 0.1.1 is tagged `compliance-assistant--v0.1.1`: <https://github.com/noru-tech/compliance-assistant/tags>. Gap: 0.1.0 has no tag, and the changelog's compare links use `v0.1.1` and `v0.1.0`, which do not match the tag name. |
| `release_notes` | MUST | Met | Keep a Changelog format, written by hand, one section per release: <https://github.com/noru-tech/compliance-assistant/blob/main/CHANGELOG.md> |
| `release_notes_vulns` | MUST | N/A | No publicly known vulnerabilities have been fixed in any release. |

## Reporting

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `report_process` | MUST | Met | Bug report and feature request forms: <https://github.com/noru-tech/compliance-assistant/issues/new/choose> |
| `report_tracker` | SHOULD | Met | GitHub Issues: <https://github.com/noru-tech/compliance-assistant/issues> |
| `report_responses` | MUST | Met | No bug reports have been filed (zero issues as of 2026-10-01), so none is unacknowledged. Revisit once reports arrive. |
| `enhancement_responses` | SHOULD | Met | No enhancement requests have been filed yet. |
| `report_archive` | MUST | Met | GitHub Issues is public and searchable: <https://github.com/noru-tech/compliance-assistant/issues?q=is%3Aissue> |
| `vulnerability_report_process` | MUST | Met | <https://github.com/noru-tech/compliance-assistant/blob/main/SECURITY.md#reporting-a-vulnerability> |
| `vulnerability_report_private` | MUST | Met | GitHub Private Vulnerability Reporting, or email to security@noru.tech: <https://github.com/noru-tech/compliance-assistant/blob/main/SECURITY.md#reporting-a-vulnerability> |
| `vulnerability_report_response` | MUST | N/A | No vulnerability reports in the last 6 months. SECURITY.md commits to acknowledging within 5 business days. |

## Quality

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `build` | MUST | N/A | Nothing is built. Clients install the Markdown and JSON files as they are in git. |
| `build_common_tools` | SUGGESTED | N/A | No build. |
| `build_floss_tools` | SHOULD | N/A | No build. |
| `test` | MUST | Met | `scripts/check_repo.py` is an MIT-licensed, stdlib-only automated check of the marketplace and plugin manifests, MCP configuration, registry entry, skill frontmatter, version consistency and secret hygiene. How to run it: <https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md#development--testing>. It validates structure. It does not test the skill's behaviour inside an AI client. |
| `test_invocation` | SHOULD | Unmet | The check runs as `python3 scripts/check_repo.py`, not through a standard runner such as `python3 -m unittest`. |
| `test_most` | SUGGESTED | Unmet | Every manifest and config file is covered. The skill is natural-language instructions, which the check cannot exercise. |
| `test_continuous_integration` | SUGGESTED | Met | `.github/workflows/check.yml` runs `scripts/check_repo.py` on every pull request and push to `main`: <https://github.com/noru-tech/compliance-assistant/blob/main/.github/workflows/check.yml> |
| `test_policy` | MUST | Met | CONTRIBUTING.md "Test policy": a change that adds a manifest, field or checkable behaviour must add the matching check to `scripts/check_repo.py` in the same pull request: <https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md#development--testing> |
| `tests_are_added` | MUST | Met | Each new manifest came with checks. The MCP Registry, Gemini CLI and Cursor manifests were added together with checks for them in #9 (<https://github.com/noru-tech/compliance-assistant/commit/90104e6>). The checker itself was added in <https://github.com/noru-tech/compliance-assistant/commit/4193b59>. |
| `tests_documented_added` | SUGGESTED | Met | The test policy is in the contribution instructions: <https://github.com/noru-tech/compliance-assistant/blob/main/CONTRIBUTING.md#development--testing> |
| `warnings` | MUST | Met | The shipped payload is JSON and Markdown with YAML frontmatter. `scripts/check_repo.py` acts as its linter: it parses every manifest and checks required fields, paths, endpoint and versions. CodeQL also analyses the Python and workflow code. No Python linter such as ruff runs on the checker itself. |
| `warnings_fixed` | MUST | Met | The check exits non-zero on any finding, and `main` passes. |
| `warnings_strict` | SUGGESTED | Met | Every finding fails the check. There is no warning-only level. |

## Security

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `know_secure_design` | MUST | Met | Maintainer attestation, to be confirmed by whoever submits. The design reflects it: least-privilege scopes, no stored credentials, no inline auth headers, write actions only after explicit confirmation. <https://github.com/noru-tech/compliance-assistant/blob/main/SECURITY.md#threat-model> |
| `know_common_errors` | MUST | Met | Maintainer attestation. The threat model names the main risks for this kind of package (leaked tokens, over-broad scopes, accidental writes, data in logs) and the mitigations: <https://github.com/noru-tech/compliance-assistant/blob/main/SECURITY.md#threat-model> |
| `crypto_published` | MUST | N/A | The project implements and calls no cryptography. TLS to the MCP endpoint and OAuth are handled by the user's MCP client and Noru's server. |
| `crypto_call` | SHOULD | N/A | As above. |
| `crypto_floss` | MUST | N/A | As above. |
| `crypto_keylength` | MUST | N/A | As above. |
| `crypto_working` | MUST | N/A | As above. |
| `crypto_weaknesses` | SHOULD | N/A | As above. |
| `crypto_pfs` | SHOULD | N/A | As above. |
| `crypto_password_storage` | MUST | N/A | The project stores no passwords or credentials. |
| `crypto_random` | MUST | N/A | The project generates no keys or nonces. |
| `delivery_mitm` | MUST | Met | Clients install from GitHub over HTTPS (`/plugin marketplace add`, `codex plugin marketplace add`, `copilot plugin marketplace add`, `gemini extensions install https://...`). |
| `delivery_unsigned` | MUST | Met | No hash is fetched over HTTP. The registry publish workflow pins `mcp-publisher`'s SHA-256 in the repository and checks the download against it: <https://github.com/noru-tech/compliance-assistant/blob/main/.github/workflows/publish-mcp-registry.yml> |
| `vulnerabilities_fixed_60_days` | MUST | Met | No known vulnerabilities. The payload has no dependencies. GitHub Actions are pinned by SHA and updated by Dependabot. |
| `vulnerabilities_critical_fixed` | SHOULD | Met | No critical vulnerabilities have been reported. |
| `no_leaked_credentials` | MUST | Met | Only placeholders are committed (`<NORU_API_KEY>`, `.env.example`). `scripts/check_repo.py` fails on secret-like values, and a scan of the full git history found none. <https://github.com/noru-tech/compliance-assistant/blob/main/SECURITY.md#secret-handling> |

## Analysis

| Criterion | Level | Answer | Evidence and justification |
| --- | --- | --- | --- |
| `static_analysis` | MUST | Met | CodeQL analyses the Python (`scripts/check_repo.py`) and GitHub Actions workflows on every pull request, on `main` and weekly: <https://github.com/noru-tech/compliance-assistant/blob/main/.github/workflows/codeql.yml>. The installed payload has no code to analyse. |
| `static_analysis_common_vulnerabilities` | SUGGESTED | Met | CodeQL's default query suites look for common vulnerabilities, including workflow injection in Actions. |
| `static_analysis_fixed` | MUST | Met | No confirmed medium or higher findings. Check the repository's code scanning alerts before submitting. |
| `static_analysis_often` | SUGGESTED | Met | On every pull request and push to `main`, plus weekly. |
| `dynamic_analysis` | SUGGESTED | Unmet | Nothing to run. The payload is Markdown and JSON, and N/A is not allowed for this criterion. |
| `dynamic_analysis_unsafe` | SUGGESTED | N/A | No memory-unsafe languages. |
| `dynamic_analysis_enable_assertions` | SUGGESTED | Unmet | No dynamic analysis. |
| `dynamic_analysis_fixed` | MUST | N/A | No dynamic analysis, so no findings to fix. |
