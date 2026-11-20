#!/usr/bin/env python3
"""Validate the public compliance-assistant repository structure.

This check is intentionally standard-library only. It does not hit the network,
install dependencies, or read outside the repository.
"""

from __future__ import annotations

import json
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = ROOT / "plugins" / "compliance-assistant"
ENDPOINT_OVERRIDE_ENV = "NORU_" + "API_URL"

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)

SECRET_PATTERNS = [
    re.compile(r"noru_[A-Za-z0-9]{16,}"),
    re.compile(r"Bearer [A-Za-z0-9][A-Za-z0-9._-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{16,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{16,}"),
]
# File types Anthropic's plugin directory accepts from organizations that are not Verified:
# Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO images. No .svg (not even for icons in
# other tools' manifests), no scripts, nothing that starts with #!.
DIRECTORY_ALLOWED_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Frontmatter keys allowed by the Agent Skills specification (agentskills.io/specification),
# which Claude Code, Codex and claude.ai uploads all accept. Anything else (e.g. `version`)
# belongs under `metadata`.
SKILL_FRONTMATTER_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKILL_TOOL_RE = re.compile(r"`noru:([A-Za-z]+)`")
TOOLS_REFERENCE = PLUGIN_ROOT / "skills" / "compliance-assistant" / "references" / "tools.md"
LOCAL_USER_PATH_RE =re.compile(r"/" + "Users" + r"/[^\s\"'`]+")

TEXT_SUFFIXES = {
    "",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".example",
    ".gitignore",
}


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return payload


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_codex_marketplace(errors: list[str]) -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    payload = load_json(path, errors)
    plugins = payload.get("plugins")

    require(payload.get("name") == "compliance-assistant", "Codex marketplace name must be compliance-assistant", errors)
    require(isinstance(payload.get("interface"), dict), "Codex marketplace must include interface object", errors)
    require(isinstance(plugins, list) and len(plugins) == 1, "Codex marketplace must contain exactly one plugin", errors)

    if not isinstance(plugins, list) or not plugins:
        return

    entry = plugins[0]
    source = entry.get("source") if isinstance(entry, dict) else None
    policy = entry.get("policy") if isinstance(entry, dict) else None

    require(entry.get("name") == "compliance-assistant", "Codex plugin entry name must be compliance-assistant", errors)
    require(isinstance(source, dict), "Codex plugin entry must include source object", errors)
    if isinstance(source, dict):
        require(source.get("source") == "local", "Codex plugin source.source must be local", errors)
        require(source.get("path") == "./plugins/compliance-assistant", "Codex plugin source.path must point at ./plugins/compliance-assistant", errors)
        require((ROOT / "plugins" / "compliance-assistant").is_dir(), "Codex plugin source.path target must exist", errors)
    require(isinstance(policy, dict), "Codex plugin entry must include policy object", errors)
    if isinstance(policy, dict):
        require(policy.get("installation") == "AVAILABLE", "Codex policy.installation must be AVAILABLE", errors)
        require(policy.get("authentication") == "ON_INSTALL", "Codex policy.authentication must be ON_INSTALL", errors)
    require(isinstance(entry.get("category"), str) and entry["category"], "Codex plugin entry must include category", errors)


def validate_codex_plugin(errors: list[str]) -> None:
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json", errors)
    require(manifest.get("name") == "compliance-assistant", "Codex plugin name must be compliance-assistant", errors)
    require(isinstance(manifest.get("version"), str) and SEMVER_RE.fullmatch(manifest["version"]) is not None, "Codex plugin version must be semver", errors)
    require(manifest.get("skills") == "./skills/", "Codex plugin skills path must be ./skills/", errors)
    require(manifest.get("mcpServers") == "./.mcp.json", "Codex plugin mcpServers path must be ./.mcp.json", errors)
    require((PLUGIN_ROOT / "skills" / "compliance-assistant" / "SKILL.md").is_file(), "Codex plugin skill file must exist", errors)
    require((PLUGIN_ROOT / ".mcp.json").is_file(), "Codex plugin .mcp.json must exist", errors)

    interface = manifest.get("interface")
    require(isinstance(interface, dict), "Codex plugin must include interface object", errors)
    if isinstance(interface, dict):
        # Limits from the OpenAI plugin directory submission rules
        # (developers.openai.com/plugins/deploy/submission).
        limits = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80, "category": 80}
        for field, limit in limits.items():
            value = interface.get(field)
            require(isinstance(value, str) and 0 < len(value) <= limit, f"Codex interface.{field} must be 1-{limit} characters", errors)
        capabilities = interface.get("capabilities")
        require(
            isinstance(capabilities, list) and 0 < len(capabilities) <= 20 and all(isinstance(item, str) and 0 < len(item) <= 120 for item in capabilities),
            "Codex interface.capabilities must be 1-20 strings of at most 120 characters",
            errors,
        )
        prompts = interface.get("defaultPrompt")
        require(
            isinstance(prompts, list)
            and 0 < len(prompts) <= 3
            and len(set(prompts)) == len(prompts)
            and all(isinstance(item, str) and 0 < len(item) <= 128 for item in prompts),
            "Codex interface.defaultPrompt must be a list of 1-3 unique prompts of at most 128 characters",
            errors,
        )
        for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
            value = interface.get(field)
            require(isinstance(value, str) and value.startswith("https://") and len(value) <= 1024, f"Codex interface.{field} must be an https URL", errors)
        for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
            value = interface.get(field)
            if value is None and field.endswith("Dark"):
                continue
            require(isinstance(value, str) and value.startswith("./") and (PLUGIN_ROOT / value).is_file(), f"Codex interface.{field} must be a ./ path to an existing file", errors)
        for field in ("brandColor", "brandColorDark"):
            value = interface.get(field)
            if value is not None:
                require(isinstance(value, str) and HEX_COLOR_RE.fullmatch(value) is not None, f"Codex interface.{field} must be a #RRGGBB color", errors)
        onboarding = interface.get("onboardingSkill")
        require(isinstance(onboarding, str) and (PLUGIN_ROOT / onboarding).is_file(), "Codex interface.onboardingSkill must point at an existing SKILL.md", errors)


def validate_claude_metadata(errors: list[str]) -> None:
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    plugins = marketplace.get("plugins")

    require(marketplace.get("name") == "compliance-assistant", "Claude marketplace name must be compliance-assistant", errors)
    require(isinstance(plugins, list) and len(plugins) == 1, "Claude marketplace must contain exactly one plugin", errors)
    if isinstance(plugins, list) and plugins:
        entry = plugins[0]
        require(entry.get("name") == "compliance-assistant", "Claude plugin entry name must be compliance-assistant", errors)
        require(entry.get("source") == "./plugins/compliance-assistant", "Claude plugin source must point at ./plugins/compliance-assistant", errors)
        require(entry.get("version") == manifest.get("version"), "Claude marketplace version must match plugin manifest", errors)

    require(manifest.get("name") == "compliance-assistant", "Claude plugin manifest name must be compliance-assistant", errors)
    require(manifest.get("displayName") == "Noru Compliance Assistant", "Claude displayName must be Noru Compliance Assistant", errors)
    require("category" not in manifest, "Claude plugin.json has no category field; set category on the marketplace entry", errors)
    # Fields read by Anthropic's plugin directory (code.claude.com/docs/en/plugins/manifest-reference).
    icon = manifest.get("icon")
    require(isinstance(icon, str) and icon.startswith("./") and (PLUGIN_ROOT / icon).is_file(), "Claude plugin icon must be a ./ path to an existing image", errors)
    for field in ("homepage", "documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
        value = manifest.get(field)
        require(isinstance(value, str) and value.startswith("https://"), f"Claude plugin {field} must be an https URL", errors)
    codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json", errors)
    codex_interface = codex.get("interface") if isinstance(codex.get("interface"), dict) else {}
    require(manifest.get("privacyPolicyUrl") == codex_interface.get("privacyPolicyURL"), "Claude and Codex privacy policy URLs must match", errors)
    require(manifest.get("termsOfServiceUrl") == codex_interface.get("termsOfServiceURL"), "Claude and Codex terms of service URLs must match", errors)
    require(manifest.get("version") == codex.get("version"), "Claude and Codex plugin versions must match", errors)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)} must start with YAML frontmatter")
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)} frontmatter must be closed")
        return {}

    # Minimal YAML subset: top-level `key: value` pairs, plus one level of indented
    # `key: value` pairs under a key with an empty value (e.g. `metadata:`).
    values: dict[str, object] = {}
    parent: str | None = None
    for raw in text[4:end].splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{path.relative_to(ROOT)} frontmatter line is invalid: {raw}")
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        value = value.strip("\"'")
        if raw[:1] in (" ", "\t"):
            if parent is None or not isinstance(values.get(parent), dict):
                errors.append(f"{path.relative_to(ROOT)} frontmatter line is indented without a parent key: {raw}")
                continue
            values[parent][key] = value  # type: ignore[index]
            continue
        if value:
            values[key] = value
            parent = None
        else:
            values[key] = {}
            parent = key
    return values


def validate_skills(errors: list[str]) -> None:
    """Check every skill against the Agent Skills spec and the live-tool snapshot."""
    manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    skills_dir = PLUGIN_ROOT / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}
    require({"compliance-assistant", "noru-setup"} <= names, "skills must include compliance-assistant and noru-setup", errors)

    known_tools: set[str] = set()
    if TOOLS_REFERENCE.is_file():
        known_tools = set(re.findall(r"`([a-z][A-Za-z]+)`", TOOLS_REFERENCE.read_text(encoding="utf-8")))
    else:
        errors.append(f"missing {TOOLS_REFERENCE.relative_to(ROOT)}")

    for path in skill_files:
        rel = path.relative_to(ROOT)
        frontmatter = parse_frontmatter(path, errors)
        unknown = set(frontmatter) - SKILL_FRONTMATTER_KEYS
        require(not unknown, f"{rel} has frontmatter keys outside the Agent Skills spec: {sorted(unknown)} (put them under metadata)", errors)
        name = frontmatter.get("name")
        require(name == path.parent.name, f"{rel} name must match its folder name", errors)
        require(isinstance(name, str) and len(name) <= 64 and SKILL_NAME_RE.fullmatch(name) is not None, f"{rel} name must be lowercase letters, digits and single hyphens, at most 64 characters", errors)
        require(isinstance(name, str) and "claude" not in name and "anthropic" not in name, f"{rel} name must not contain reserved words", errors)
        description = frontmatter.get("description")
        require(isinstance(description, str) and 0 < len(description) <= 1024, f"{rel} description must be 1-1024 characters", errors)
        require(isinstance(description, str) and "Use when" in description, f"{rel} description must say when to use the skill (\"Use when ...\")", errors)
        metadata = frontmatter.get("metadata")
        require(isinstance(metadata, dict) and metadata.get("version") == manifest.get("version"), f"{rel} metadata.version must match the plugin version", errors)

        lines = path.read_text(encoding="utf-8").count("\n")
        require(lines <= 500, f"{rel} must stay under 500 lines; move detail into references/", errors)

        texts = [path] + sorted(path.parent.glob("references/*.md"))
        for doc in texts:
            content = doc.read_text(encoding="utf-8")
            for tool in set(SKILL_TOOL_RE.findall(content)) - {"toolName"}:
                require(tool in known_tools, f"{doc.relative_to(ROOT)} mentions noru:{tool}, which is not in references/tools.md", errors)
            for link in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", content):
                if "://" in link:
                    continue
                require((doc.parent / link).resolve().is_file(), f"{doc.relative_to(ROOT)} links to missing file {link}", errors)

        openai_yaml = path.parent / "agents" / "openai.yaml"
        require(openai_yaml.is_file(), f"{rel} needs agents/openai.yaml for Codex skill metadata", errors)
        if openai_yaml.is_file():
            content = openai_yaml.read_text(encoding="utf-8")
            require(f"${path.parent.name}" in content, f"{openai_yaml.relative_to(ROOT)} default_prompt must mention ${path.parent.name}", errors)
            require('value: "noru"' in content, f"{openai_yaml.relative_to(ROOT)} must declare the noru MCP dependency", errors)
            for icon in re.findall(r'icon_(?:small|large):\s*"([^"]+)"', content):
                require((PLUGIN_ROOT / icon).is_file(), f"{openai_yaml.relative_to(ROOT)} icon {icon} must exist in the plugin root", errors)


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def validate_directory_policy(errors: list[str]) -> None:
    """Rules the Anthropic plugin directory enforces for organizations that are not Verified."""
    for path in sorted(PLUGIN_ROOT.rglob("*")):
        if path.is_dir() or path.name == ".DS_Store":
            continue
        rel = path.relative_to(ROOT)
        require(path.suffix.lower() in DIRECTORY_ALLOWED_SUFFIXES, f"{rel}: the plugin directory only accepts Markdown, text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO files from unverified organizations", errors)
        if path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"}:
            raw = path.read_bytes()
            require(not raw.startswith(b"#!"), f"{rel} must not start with #!", errors)
            require(b"\x00" not in raw, f"{rel} must not contain NUL bytes", errors)
            try:
                raw.decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"{rel} must be UTF-8")

    manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    icon = manifest.get("icon")
    if isinstance(icon, str) and (PLUGIN_ROOT / icon).is_file():
        icon_path = PLUGIN_ROOT / icon
        size = png_size(icon_path)
        require(size is not None, "Claude plugin icon must be a PNG", errors)
        if size is not None:
            width, height = size
            require(width == height and 512 <= width <= 2048, f"Claude plugin icon must be a square PNG of 512-2048 px (is {width}x{height})", errors)
        require(icon_path.stat().st_size < 2 * 1024 * 1024, "Claude plugin icon must be under 2 MB", errors)


def validate_mcp(errors: list[str]) -> None:
    payload = load_json(PLUGIN_ROOT / ".mcp.json", errors)
    servers = payload.get("mcpServers")
    require(isinstance(servers, dict), ".mcp.json must include mcpServers object", errors)
    if isinstance(servers, dict):
        noru = servers.get("noru")
        require(isinstance(noru, dict), ".mcp.json must include noru server", errors)
        if isinstance(noru, dict):
            require(noru.get("type") == "http", "noru MCP server type must be http", errors)
            require(noru.get("url") == "https://api.noru.tech/v1/mcp", "noru MCP server URL must be production endpoint", errors)
            require("headers" not in noru, "committed .mcp.json must not inline auth headers, which would disable OAuth", errors)
            unknown = set(noru) - {"type", "url"}
            require(not unknown, f".mcp.json noru server has non-standard keys {sorted(unknown)}; document auth in the client guides instead", errors)


def validate_registry_server(errors: list[str]) -> None:
    """Check server.json, the official MCP Registry entry for the remote server.

    Field names and limits follow the registry's 2025-12-11 server.json schema
    (modelcontextprotocol/registry internal/validators/schemas/2025-12-11.json).
    """
    payload = load_json(ROOT / "server.json", errors)
    if not payload:
        return
    manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    description = payload.get("description")

    require(payload.get("$schema") == "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json", "server.json $schema must be the 2025-12-11 registry schema", errors)
    require(payload.get("name") == "tech.noru/mcp", "server.json name must be tech.noru/mcp", errors)
    require(isinstance(description, str) and 1 <= len(description) <= 100, "server.json description must be 1-100 characters", errors)
    require(payload.get("version") == manifest.get("version"), "server.json version must match plugin manifest", errors)
    require("packages" not in payload, "server.json describes the remote server only and must not list packages", errors)

    remotes = payload.get("remotes")
    require(isinstance(remotes, list) and len(remotes) == 1, "server.json must contain exactly one remote", errors)
    if isinstance(remotes, list) and remotes and isinstance(remotes[0], dict):
        remote = remotes[0]
        require(remote.get("type") == "streamable-http", "server.json remote type must be streamable-http", errors)
        require(remote.get("url") == "https://api.noru.tech/v1/mcp", "server.json remote URL must be production endpoint", errors)
        for header in remote.get("headers", []):
            require(header.get("isSecret") is True, "server.json remote headers must be marked isSecret", errors)
            require(header.get("isRequired") is False, "server.json auth header must be optional so OAuth clients need no API key", errors)


def validate_cursor_metadata(errors: list[str]) -> None:
    """Check the Cursor plugin layout (cursor/plugins schemas/*.schema.json)."""
    marketplace = load_json(ROOT / ".cursor-plugin" / "marketplace.json", errors)
    manifest = load_json(PLUGIN_ROOT / ".cursor-plugin" / "plugin.json", errors)
    claude_manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    plugins = marketplace.get("plugins")

    require(marketplace.get("name") == "compliance-assistant", "Cursor marketplace name must be compliance-assistant", errors)
    require(isinstance(plugins, list) and len(plugins) == 1, "Cursor marketplace must contain exactly one plugin", errors)
    if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
        entry = plugins[0]
        require(entry.get("name") == "compliance-assistant", "Cursor plugin entry name must be compliance-assistant", errors)
        require(entry.get("source") == "./plugins/compliance-assistant", "Cursor plugin source must point at ./plugins/compliance-assistant", errors)

    require(manifest.get("name") == "compliance-assistant", "Cursor plugin manifest name must be compliance-assistant", errors)
    require(manifest.get("version") == claude_manifest.get("version"), "Cursor plugin version must match Claude plugin manifest", errors)
    require(manifest.get("skills") == "./skills/", "Cursor plugin skills path must be ./skills/", errors)
    require(manifest.get("mcpServers") == "./mcp.json", "Cursor plugin mcpServers path must be ./mcp.json", errors)

    cursor_mcp = load_json(PLUGIN_ROOT / "mcp.json", errors)
    servers = cursor_mcp.get("mcpServers")
    noru = servers.get("noru") if isinstance(servers, dict) else None
    require(isinstance(noru, dict), "Cursor mcp.json must include noru server", errors)
    if isinstance(noru, dict):
        require(noru.get("type") == "http", "Cursor noru MCP server type must be http", errors)
        require(noru.get("url") == "https://api.noru.tech/v1/mcp", "Cursor noru MCP server URL must be production endpoint", errors)
        require("headers" not in noru, "Cursor mcp.json must not inline auth headers", errors)


def validate_gemini_extension(errors: list[str]) -> None:
    """Check gemini-extension.json (google-gemini/gemini-cli docs/extensions/reference.md)."""
    payload = load_json(ROOT / "gemini-extension.json", errors)
    manifest = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json", errors)
    require(payload.get("name") == "compliance-assistant", "Gemini extension name must be compliance-assistant", errors)
    require(payload.get("version") == manifest.get("version"), "Gemini extension version must match plugin manifest", errors)

    context = payload.get("contextFileName")
    require(isinstance(context, str) and (ROOT / context).is_file(), "Gemini contextFileName must point at an existing file", errors)

    servers = payload.get("mcpServers")
    noru = servers.get("noru") if isinstance(servers, dict) else None
    require(isinstance(noru, dict), "Gemini extension must include noru MCP server", errors)
    if isinstance(noru, dict):
        require(noru.get("httpUrl") == "https://api.noru.tech/v1/mcp", "Gemini noru httpUrl must be production endpoint", errors)
        require("headers" not in noru, "Gemini extension must not inline auth headers", errors)


def validate_env_example(errors: list[str]) -> None:
    path = ROOT / ".env.example"
    if not path.is_file():
        errors.append("missing .env.example")
        return
    text = path.read_text(encoding="utf-8")
    require("NORU_API_KEY=<your_noru_api_key>" in text, ".env.example must use NORU_API_KEY placeholder", errors)
    require(ENDPOINT_OVERRIDE_ENV not in text, ".env.example must only include the required API key placeholder", errors)
    for pattern in SECRET_PATTERNS:
        require(pattern.search(text) is None, ".env.example must not contain realistic secret-looking values", errors)


def scan_for_secrets(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {".env.example", ".gitignore"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel} contains a realistic secret-looking value matching {pattern.pattern}")
        if LOCAL_USER_PATH_RE.search(text):
            errors.append(f"{rel} contains an absolute local user path")


def main() -> int:
    errors: list[str] = []
    validate_codex_marketplace(errors)
    validate_codex_plugin(errors)
    validate_claude_metadata(errors)
    validate_skills(errors)
    validate_directory_policy(errors)
    validate_mcp(errors)
    validate_registry_server(errors)
    validate_cursor_metadata(errors)
    validate_gemini_extension(errors)
    validate_env_example(errors)
    scan_for_secrets(errors)

    if errors:
        print("Repository checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: repository marketplace, plugin metadata, MCP config, registry entry, Cursor and Gemini manifests, skill, and secret hygiene checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
