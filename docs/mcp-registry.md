# Publishing to the official MCP Registry

[`server.json`](../server.json) describes Noru's remote MCP server for the official MCP Registry
(`registry.modelcontextprotocol.io`) under the name `tech.noru/mcp`. The
[`publish-mcp-registry`](../.github/workflows/publish-mcp-registry.yml) workflow publishes it. It
runs only when started by hand, on `main`.

The listing is for the **server** at `https://api.noru.tech/v1/mcp`, not for this plugin. The plugin
is distributed through the Claude Code and Codex marketplaces described in the [README](../README.md).

Sources: `modelcontextprotocol/registry` at commit `bf4e88cbe8d1a635c06144ccea1d24cb52fa6186`,
files `docs/modelcontextprotocol-io/authentication.mdx`, `remote-servers.mdx`, `github-actions.mdx`,
`versioning.mdx`, `docs/reference/cli/commands.md` and the `2025-12-11` schema at
`internal/validators/schemas/2025-12-11.json`.

## Why DNS authentication

The registry ties the name to the way you sign in. `login github-oidc` (GitHub Actions) only grants
`io.github.<repository owner>/*`. Only domain authentication grants `tech.noru/*`, so the workflow
uses `login dns --domain noru.tech`. DNS sign-in grants `tech.noru/*` and `tech.noru.*/*`.

## One-time setup

### 1. Generate the key pair

Run this on a trusted machine with OpenSSL 3.0 or later. The macOS system `openssl` (LibreSSL) has
no Ed25519 support, so on a Mac use `brew install openssl@3` and run that binary instead.

```bash
MY_DOMAIN="noru.tech"

# Generate public/private key pair using Ed25519
openssl genpkey -algorithm Ed25519 -out key.pem

# Generate TXT record
PUBLIC_KEY="$(openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64)"
echo "${MY_DOMAIN}. IN TXT \"v=MCPv1; k=ed25519; p=${PUBLIC_KEY}\""
```

### 2. Add the DNS TXT record

Add a TXT record at the **apex** of `noru.tech`. Do not put it under a selector such as
`_mcp-auth.noru.tech`, because the registry only reads the apex. Keep any existing apex TXT
records, such as SPF:

```text
noru.tech. IN TXT "v=MCPv1; k=ed25519; p=<PUBLIC_KEY from step 1>"
```

Check that it has propagated:

```bash
dig +short TXT noru.tech | grep 'v=MCPv1'
```

When you rotate the key, delete the old `v=MCPv1` record. The registry tries a stale record first,
and verification then fails.

### 3. Add the private key as a secret

Print the private key as the hex string that `mcp-publisher login dns --private-key` expects:

```bash
openssl pkey -in key.pem -noout -text | grep -A3 "priv:" | tail -n +2 | tr -d ' :\n'
```

In GitHub, open **Settings → Secrets and variables → Actions** for `noru-tech/compliance-assistant`
and add a secret named `MCP_REGISTRY_PRIVATE_KEY` containing that 64-character hex value. Then
store `key.pem` in Noru's secret manager, or delete it. Never commit it.

Recommended hardening, as the registry's GitHub Actions guide advises: the job runs in the
`mcp-registry-publish` environment. Under **Settings → Environments → mcp-registry-publish**, limit
deployment branches to `main` and add yourself as a required reviewer. You can also store
`MCP_REGISTRY_PRIVATE_KEY` as a secret on that environment instead of on the repository. The job
reads it either way.

## Publish

1. Check that `version` in `server.json` has never been published. Each published version is
   immutable and must be unique.
2. Go to **Actions → publish-mcp-registry → Run workflow**, choose branch `main`, and run it.
3. The job installs `mcp-publisher` 1.8.1 and verifies its SHA-256. It then validates `server.json`,
   signs in with DNS for `noru.tech`, publishes, and logs out.

To run the same steps locally instead:

```bash
mcp-publisher validate server.json
mcp-publisher login dns --domain noru.tech --private-key "$(openssl pkey -in key.pem -noout -text | grep -A3 "priv:" | tail -n +2 | tr -d ' :\n')"
mcp-publisher publish server.json
```

## Verify the listing

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=tech.noru/mcp"
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers/tech.noru%2Fmcp/versions/latest"
```

Both should return `"name": "tech.noru/mcp"`, the version you published, and the
`https://api.noru.tech/v1/mcp` remote.

## Versioning

`server.json` uses the plugin version (`0.1.1`), and `scripts/check_repo.py` keeps the two in step.
The registry's versioning guide recommends tying a remote server's version to its API version.
Noru's endpoint shows only a major path segment (`/v1`), not a release version, so the repository's
release version is the closest stable identifier. Every publish needs a new version. If `0.1.1` is
already listed and only the metadata changes, release a new plugin version rather than a
prerelease. A prerelease such as `0.1.1-1` sorts before `0.1.1`, so it would not be marked latest.
