#!/bin/sh
# Builds the ZIP for the OpenAI plugin portal (platform.openai.com/plugins).
# It holds only what Codex reads, under a single compliance-assistant/ folder:
# .codex-plugin/, .mcp.json, assets/ and skills/. The eval suite and the other
# clients' manifests are left out.
#
# The ZIP's .mcp.json comes from packaging/codex/mcp.json, which declares OAuth
# for the OpenAI portal (extensions.com.openai.auth). It is kept outside the
# plugin folder because Claude Code and Anthropic's plugin directory reject
# unknown keys in the plugin's own .mcp.json.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
plugin="$root/plugins/compliance-assistant"
version=$(sed -n 's/.*"version": "\([^"]*\)".*/\1/p' "$plugin/.codex-plugin/plugin.json" | head -1)
out="${1:-$root/dist/compliance-assistant-codex-$version.zip}"
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/compliance-assistant" "$(dirname "$out")"
cp -R "$plugin/.codex-plugin" "$plugin/assets" "$plugin/skills" "$stage/compliance-assistant/"
cp "$root/packaging/codex/mcp.json" "$stage/compliance-assistant/.mcp.json"
rm -f "$out"
(cd "$stage" && zip -qrX "$out" compliance-assistant -x '*.DS_Store')
echo "$out"
