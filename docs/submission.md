# Plugin directory submission

What this repository already provides for listing `compliance-assistant` in the Anthropic and
OpenAI plugin directories, and what still needs a person at Noru. Your own marketplaces (`/plugin
marketplace add`, `codex plugin marketplace add`) work without any of this.

## Already in the repository

| Item | Where |
| --- | --- |
| Display name, description, keywords | `plugins/compliance-assistant/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` |
| Icon / logo, composer icon | `plugins/compliance-assistant/assets/`: `logo.png` 1024 px, `composer-icon.png` 256 px, both square PNGs (source: `packaging/brand/signum-dark.svg`) |
| Website, documentation, support, privacy, terms URLs | both plugin manifests |
| Starter prompts (at most 3, each at most 128 characters) | Codex `interface.defaultPrompt` |
| Onboarding skill | `skills/noru-setup/` (Codex `interface.onboardingSkill`) |
| README of at least 40 words, MIT licence | `README.md`, `LICENSE` |
| Remote MCP server with OAuth and no inline headers | `plugins/compliance-assistant/.mcp.json` |
| Review test cases: 5 positive, 3 negative | `plugins/compliance-assistant/evals/` |
| Automated validation | `python3 scripts/check_repo.py`, `claude plugin validate --strict` (CI) |

## Anthropic plugin directory

Noru is not a Verified organization in the directory, so the plugin folder may only contain Markdown,
text, JSON, YAML and PNG/JPEG/GIF/WebP/ICO files. That means no `.svg`, no scripts and nothing
starting with `#!`. The icon must be a square PNG or JPEG of 512 to 2048 px, under 2 MB. The
directory only adopts the icon the first time the plugin is saved or submitted, so if the listing
still has no icon, set it under **Edit** on the submission. `scripts/check_repo.py` enforces these
rules.

Source: <https://claude.com/docs/plugins/submit>, pre-submission checklist at
<https://claude.com/docs/plugins/pre-submission-checklist>.

1. Run `claude plugin validate --strict plugins/compliance-assistant` and fix every finding.
2. At claude.ai/directory/manage, choose **Submit new** → **Plugin bundle**, point it at
   `noru-tech/compliance-assistant` with plugin path `plugins/compliance-assistant`, and install the
   Claude GitHub App when prompted.
3. Click **Validate** and check the listing details it reads from `plugin.json` and the README.
4. Answer the data-handling questions. The plugin itself stores nothing; all data stays in Noru,
   reached through the customer's own authenticated MCP connection.
5. Give a contact email, accept the acknowledgements, and submit. The repository must be public to
   publish.

## OpenAI plugin directory (ChatGPT and Codex)

Source: <https://developers.openai.com/plugins/deploy/submission>.

1. An organization admin grants Apps Management **Write** to the submitter.
2. At platform.openai.com/plugins, choose **Upload new or existing plugin** and upload the ZIP. Build
   it with `scripts/build_codex_zip.sh`, which packages only what Codex reads: `.codex-plugin/`,
   `.mcp.json`, `assets/` and `skills/`.
3. **Domain verification:** serve the portal's token as plain text at
   `https://api.noru.tech/.well-known/openai-apps-challenge` (or on a parent domain).
4. **Auth:** OAuth only for public listing. The API-key path in the client guides is for manual
   setups and is not part of the submission.
5. **Review test cases:** already in `.codex-plugin/plugin.json` under
   `extensions.com.openai.review` (5 positive, 3 negative), so the portal imports them from the ZIP.
   Enter reviewer credentials for a demo Noru organization in **Review details**, never in the ZIP.
   The account must work without MFA prompts or email codes.
6. **Demo recording:** a short video of the three starter prompts against a demo organization. Add
   its URL as `review.demo_recording_url` in the manifest, or enter it in **Review details**.
7. Optional: `logoDark`, `composerIconDark` and `brandColorDark` for dark mode, plus release notes.

## Not covered yet

- A dark-mode logo variant.
- Running the eval suite in CI. It runs offline against mocks, but it needs a model credential and
  costs about $1 a run.
