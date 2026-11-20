#!/bin/sh
# Builds the ZIP for the OpenAI plugin portal (platform.openai.com/plugins).
# It holds only what Codex reads, under a single compliance-assistant/ folder:
# .codex-plugin/, .mcp.json, assets/ and skills/. The eval suite and the other
# clients' manifests are left out.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
version=$(sed -n 's/.*"version": "\([^"]*\)".*/\1/p' "$root/plugins/compliance-assistant/.codex-plugin/plugin.json" | head -1)
out="${1:-$root/dist/compliance-assistant-codex-$version.zip}"
mkdir -p "$(dirname "$out")"
rm -f "$out"
cd "$root/plugins"
zip -qrX "$out" \
  compliance-assistant/.codex-plugin \
  compliance-assistant/.mcp.json \
  compliance-assistant/assets \
  compliance-assistant/skills \
  -x '*.DS_Store'
echo "$out"
