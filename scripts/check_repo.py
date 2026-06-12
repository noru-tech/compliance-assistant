#!/usr/bin/env python3
"""Validate the public compliance-assistant repository structure.

This check is intentionally standard-library only. It does not hit the network,
install dependencies, or read outside the repository.
"""

from __future__ import annotations

import json
import re
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
LOCAL_USER_PATH_RE = re.compile(r"/" + "Users" + r"/[^\s\"'`]+")

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
        for field in ("displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"):
            require(isinstance(interface.get(field), str) and interface[field], f"Codex interface.{field} must be non-empty", errors)
        capabilities = interface.get("capabilities")
        require(isinstance(capabilities, list) and all(isinstance(item, str) and item for item in capabilities), "Codex interface.capabilities must be non-empty strings", errors)


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

    values: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{path.relative_to(ROOT)} frontmatter line is invalid: {raw}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def validate_skill(errors: list[str]) -> None:
    frontmatter = parse_frontmatter(PLUGIN_ROOT / "skills" / "compliance-assistant" / "SKILL.md", errors)
    require(frontmatter.get("name") == "compliance-assistant", "Skill frontmatter name must be compliance-assistant", errors)
    require(bool(frontmatter.get("description")), "Skill frontmatter description must be present", errors)


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
            require("headers" not in noru, "committed .mcp.json must not inline auth headers", errors)


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
    validate_skill(errors)
    validate_mcp(errors)
    validate_env_example(errors)
    scan_for_secrets(errors)

    if errors:
        print("Repository checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: repository marketplace, plugin metadata, MCP config, skill, and secret hygiene checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
