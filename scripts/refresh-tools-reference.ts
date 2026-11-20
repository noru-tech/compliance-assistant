#!/usr/bin/env bun
/**
 * Regenerates the skill's Noru MCP tool reference from the Noru source.
 *
 *   bun scripts/refresh-tools-reference.ts <path-to-noru-checkout>
 *
 * It loads the real tool registry (apps/api/src/mcp/tools), resolves each
 * tool's scope with the server's own determineRequiredScope and its toolset
 * with toolsetForTool, then rewrites:
 *   - references/tools.md (every tool, grouped by toolset and scope)
 *   - the toolset table in references/scopes-and-toolsets.md
 *
 * Use a checkout of the commit that is deployed (normally origin/main) with
 * dependencies installed (`bun install`). Nothing here talks to the network.
 */
import { readFileSync, writeFileSync } from "node:fs"
import { join, resolve } from "node:path"

const noru = process.argv[2]
if (!noru) {
  console.error("usage: bun scripts/refresh-tools-reference.ts <path-to-noru-checkout>")
  process.exit(2)
}
const api = resolve(noru, "apps/api")
process.env.NODE_ENV ??= "test"

const { tools } = await import(join(api, "src/mcp/tools/index.ts"))
const { determineRequiredScope } = await import(join(api, "src/routes/v1/mcp.ts"))
const { toolsetForTool, TOOLSET_DESCRIPTIONS, TOOLSET_NAMES } = await import(
  join(api, "src/mcp/toolsets.ts")
)

type Row = { name: string; scope: string; toolset: string }
// A tool with `replacedBy` is never in tools/list (it only answers calls from
// older clients), so it is left out of the reference.
const rows: Row[] = Object.values(
  tools as Record<string, { name: string; segment?: string; replacedBy?: string }>
)
  .filter((tool) => !tool.replacedBy)
  .map((tool) => {
    const scope = determineRequiredScope(tool.name)
    if (!scope) throw new Error(`no scope resolves for ${tool.name}`)
    return { name: tool.name, scope, toolset: toolsetForTool(tool.name, scope, tool.segment === "tprm") }
  })

const RESOURCES: [string, string][] = [
  ["noru://frameworks/compliance-overview", "Aggregated compliance metrics for each enabled framework"],
  ["noru://policies/review-queue", "Policies in draft or review, with owners"],
  ["noru://schemas/ai-inventory-manifest", "JSON Schema for `ingestAiInventory` input"],
]

const repo = resolve(import.meta.dir, "..")
const refs = join(repo, "plugins/compliance-assistant/skills/compliance-assistant/references")
const scopeOrder = (s: string) => (s.startsWith("read:") ? 0 : 1)

const out: string[] = [
  "# Noru MCP tools by toolset",
  "",
  `Generated from the Noru source by \`scripts/refresh-tools-reference.ts\`: ${rows.length} tools in`,
  `${TOOLSET_NAMES.length} toolsets. The live list for the current connection comes from`,
  "`noru:getMcpCapabilities`, which wins over this file. A tool is listed only when the credential has",
  "its scope **and** its toolset is active (see [scopes-and-toolsets.md](scopes-and-toolsets.md)).",
  "`tprm` tools appear only for organizations with supplier risk management enabled.",
  "",
  "Every `write:` tool changes the customer's workspace. Follow [safe-actions.md](safe-actions.md) for",
  "each one.",
  "",
  "## Contents",
  "",
  ...TOOLSET_NAMES.filter((t: string) => rows.some((r) => r.toolset === t)).map(
    (t: string) => `- [${t}](#${t})`
  ),
  "- [Resources](#resources)",
  "",
]

for (const toolset of TOOLSET_NAMES as string[]) {
  const inSet = rows.filter((r) => r.toolset === toolset)
  if (inSet.length === 0) continue
  out.push(`## ${toolset}`, "", `${TOOLSET_DESCRIPTIONS[toolset]}`, "", "| Scope | Tools |", "| --- | --- |")
  const scopes = [...new Set(inSet.map((r) => r.scope))].sort(
    (a, b) => scopeOrder(a) - scopeOrder(b) || a.localeCompare(b)
  )
  for (const scope of scopes) {
    const names = inSet.filter((r) => r.scope === scope).map((r) => `\`${r.name}\``)
    out.push(`| \`${scope}\` | ${names.join(", ")} |`)
  }
  out.push("")
}

out.push("## Resources", "", "| URI | What it holds |", "| --- | --- |")
for (const [uri, what] of RESOURCES) out.push(`| \`${uri}\` | ${what} |`)
out.push("")
writeFileSync(join(refs, "tools.md"), out.join("\n"))

// Toolset table inside scopes-and-toolsets.md, between markers.
const scopesPath = join(refs, "scopes-and-toolsets.md")
const scopesDoc = readFileSync(scopesPath, "utf8")
const start = "<!-- toolsets:start -->"
const end = "<!-- toolsets:end -->"
const a = scopesDoc.indexOf(start)
const b = scopesDoc.indexOf(end)
if (a === -1 || b === -1) throw new Error(`markers ${start} / ${end} missing in ${scopesPath}`)
const table = [
  "| Toolset | Tools | Covers |",
  "| --- | --- | --- |",
  ...(TOOLSET_NAMES as string[]).map(
    (t) => `| \`${t}\` | ${rows.filter((r) => r.toolset === t).length} | ${TOOLSET_DESCRIPTIONS[t]} |`
  ),
].join("\n")
writeFileSync(scopesPath, `${scopesDoc.slice(0, a + start.length)}\n${table}\n${scopesDoc.slice(b)}`)

console.log(`wrote ${rows.length} tools in ${TOOLSET_NAMES.length} toolsets`)
