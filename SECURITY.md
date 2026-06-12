# Security Policy

## Supported Versions

This project is pre-1.0. Security fixes are applied to the latest release on the `main` branch.

| Version | Supported |
| ------- | --------- |
| 0.1.x | Yes |

## Reporting a Vulnerability

Please report security issues privately. Do not open a public issue for an unfixed vulnerability.

- Email: **security@noru.tech** with a subject line beginning `[SECURITY] compliance-assistant`.
- If hosted on GitHub, you may also use GitHub Private Vulnerability Reporting.

Please include the affected file or version, reproduction steps, expected impact, and whether any
secret or customer data exposure is involved.

We aim to acknowledge reports within 5 business days and provide a remediation timeline after triage.

## Secret Handling

This repo is public. Do not commit:

- Noru API keys or bearer tokens.
- OAuth access tokens, refresh tokens, authorization codes, or client secrets.
- Customer identifiers, organization names, audit evidence, logs, or screenshots.
- Local MCP client configs that inline secrets.
- Tool outputs captured from real customer organizations.

Authentication is managed by the MCP host or client. Use OAuth where the client supports it, or use
`NORU_API_KEY` locally for manual/headless setup. Grant the least-privilege scopes needed for the
workflow. Prefer read-only scopes for guidance-only usage, and add write scopes only when users
intentionally want the assistant to perform actions.

## Threat Model

The plugin connects local AI clients to Noru's hosted MCP endpoint. The primary risks are leaked
OAuth tokens or API keys, over-broad scopes, accidental writes through MCP tools, and disclosure of
customer compliance data in logs or examples. The skill therefore requires explicit confirmation
before write-like actions and documents least-privilege scope usage.
