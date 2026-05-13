# Marketplace & Catalog Distribution Map

Complete landscape of every public AI-agent-skill/plugin/MCP catalog this repo is published to or fits, with current status and recommended next steps.

## Status legend

| Symbol | Meaning |
|--------|---------|
| 🟢 LIVE | Already published / auto-indexed and verified |
| 🟡 OPEN | PR or submission open, awaiting review |
| 🟠 SKIPPED-VENDOR | Skipped: requires being a vendor of the underlying tech |
| 🟠 SKIPPED-FIT | Skipped: content shape doesn't fit (e.g., MCP-only) |
| 🔵 USER-ACTION | Needs human web-form submission |
| ⚪ AUTO-DISCOVERED | Auto-crawled from GitHub topics; no action needed |

---

## Tier 1 — Live and confirmed (8 surfaces)

| # | Surface | Status | Install command | Notes |
|---|---------|--------|-----------------|-------|
| 1 | **Own marketplace** (this repo) | 🟢 LIVE | `/plugin marketplace add OrcaQubits/agentic-commerce-skills-plugins` | Native Claude Code marketplace, the canonical entry point |
| 2 | **OpenClaw / ClawHub** | 🟢 LIVE | `clawhub install @ichiorca/openclaw-<plugin>` | All 15 plugins published as `@ichiorca/openclaw-*` bundle plugins |
| 3 | **Gemini CLI Extensions Gallery** | 🟢 LIVE | `gemini extensions install https://github.com/OrcaQubits/agentic-commerce-skills-plugins` | UCP flagship at v1.0.0; `gemini-cli-extension` topic set; crawler indexes daily |
| 4 | **Cursor Team Marketplace** | 🟢 LIVE | Cursor Settings → Plugins → Team Marketplaces → Import URL | `.cursor-plugin/marketplace.json` ajv-validated, 16/16 checks pass |
| 5 | **Codex CLI marketplace** | 🟢 LIVE | `codex plugin marketplace add OrcaQubits/agentic-commerce-skills-plugins` | `.agents/plugins/marketplace.json` enumerates all 15 plugins |
| 6 | **skills.sh** (Vercel) | 🟢 LIVE | `npx skills add orcaqubits/agentic-commerce-skills-plugins` | Auto-indexed (226 skills detected); badge in README; works across 56+ agents |
| 7 | **GitHub topics** | 🟢 LIVE | n/a | `claude-code-plugin`, `claude-plugin`, `cursor-plugin`, `codex-cli-plugin`, `openclaw-plugin`, `gemini-cli-extension` — drives auto-aggregators |

---

## Tier 2 — Open submissions (2 in flight)

| # | Surface | Status | URL |
|---|---------|--------|-----|
| 1 | **VoltAgent / officialskills.sh** | 🟡 OPEN | https://github.com/VoltAgent/awesome-agent-skills/pull/571 |
| 2 | **awesome-codex-cli** (RoggeOhta) | 🟡 OPEN | https://github.com/RoggeOhta/awesome-codex-cli/pull/32 |

---

## Tier 3 — Auto-indexed aggregators (probably live, verify)

These catalogs **auto-crawl GitHub** for repos with the right topics. We have all the canonical topics set, so we likely already appear:

| Surface | URL | What to verify |
|---------|-----|---------------|
| **claudemarketplaces.com** | https://claudemarketplaces.com | Search for `agentic-commerce-skills-plugins` |
| **SkillsMP** | https://skillsmp.com | Filters: min 2 stars (we have a few) |
| **LobeHub Skills** | https://lobehub.com/skills | Search by repo name |
| **agentskill.sh** | https://agentskill.sh | 110k+ skills; auto-indexed |
| **quemsah/awesome-claude-plugins** | https://github.com/quemsah/awesome-claude-plugins | n8n auto-crawls — verify our entry |
| **aitmpl.com/plugins** | https://www.aitmpl.com/plugins/ | Search |
| **awesomeskills.dev** | https://www.awesomeskills.dev/en | Search |

If any are missing us after a week, file a "please index" issue on the backing repo.

---

## Tier 4 — Worthwhile next submissions (recommended)

Ordered by leverage × effort:

### High priority

| # | Surface | Format | Why |
|---|---------|--------|-----|
| 1 | **buildwithclaude.com** | PR with component vendored into their repo's `plugins/` | Explicitly cross-vendor (Claude.ai + Claude Code + Agent SDK + OpenClaw), unusual multi-platform positioning that matches us |
| 2 | **ClaudePluginHub** + Augment Code | 🔵 Web form at https://www.claudepluginhub.com/tools/submit-plugin | Two-for-one: ClaudePluginHub feed is auto-consumed by Augment Code |
| 3 | **Goose / block/agent-skills** | PR with one or more skills vendored | Block-backed, supports multi-vendor SKILL.md; automated PR validator |

### Medium priority

| # | Surface | Format |
|---|---------|--------|
| 4 | **cursor.directory** | Submission via cursor.directory/plugins/new (third-party, distinct from cursor.com/marketplace) |
| 5 | **mcpservers.org** (combined skills + MCP catalog) | Web form |
| 6 | **agentskillexchange.com** | Web form |
| 7 | **tonsofskills.com / ccpi** | Publishing guide in [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) |
| 8 | **Agensi** (https://agensi.io) | Web form; supports paid skills + 80% rev share if monetization is ever desired |
| 9 | **PulseMCP** | Web form (MCP only — fits if you ship MCP servers) |

### Low priority / verify first

| # | Surface | Why low |
|---|---------|---------|
| **Hugging Face Skills** | Wants skills vendored into their repo; HF-themed scope; commerce content doesn't match their ML/AI focus |
| **awesome-claude-code** (hesreallyhim) | Mid-reorganization ("Update in progress"); not accepting submissions right now |
| **ComposioHQ/awesome-claude-skills / -plugins** | Both repos return 404 — may have been renamed/archived |
| **Zed extensions** | Requires Rust/WASM compilation, not SKILL.md compatible |

---

## Tier 5 — Skipped, with rationale

### Vendor-authorship gated

| Surface | Skip reason |
|---------|-------------|
| **anthropics/claude-plugins-official** (claude.com/plugins) | Anthropic curates; non-vendors face rejection (confirmed prior rejection on this repo) |
| **cursor.com/marketplace** (public Cursor marketplace) | Anysphere-reviewed; same authorship gate likely applies |
| **openai/skills** | OpenAI-curated `.system`/`.curated`/`.experimental` tiers; not a community submission target |

### MCP-only registries (we don't ship MCP servers, we ship knowledge ABOUT them)

| Surface | Skip reason |
|---------|-------------|
| Official MCP Registry | Requires actual MCP server `server.json` per server |
| Smithery.ai | MCP servers + gateway |
| Glama.ai (23k+ MCP servers) | MCP only |
| mcp.so, mcp.directory, PulseMCP | MCP catalogs |
| Cline MCP Marketplace | MCP servers only |
| Docker MCP Catalog | Containerized MCP servers only |
| punkpeye/awesome-mcp-servers, wong2/awesome-mcp-servers | MCP-only awesome-lists |

**Future opportunity**: if we extract the MCP server stubs from inside `ucp-agentic-commerce`, `acp-agentic-commerce`, `ap2-agentic-payments` into standalone MCP servers, these 7 surfaces become live targets. Today they don't fit.

### Closed / wrong content shape

| Surface | Reason |
|---------|--------|
| Sourcegraph Cody | Closed plugin model |
| Tabnine | No public plugin submission |
| Windsurf / Codeium | Distributed via VS Code marketplaces as a single extension, no plugin store |
| Aider | Auto-compatible via universal `.skilz/` fallback — no separate submission needed |
| Roo Code marketplace | Deprecated as of May 2026 |
| Replit / Bolt.new / v0 / Lovable | App-builder marketplaces, not skill registries |
| LangChain Hub | Prompt/chain-shaped, not SKILL.md packages |
| Crush | Already covered via OpenClaw bridge |

---

## Cross-platform install summary (current state)

| Command | Surface |
|---------|---------|
| `/plugin marketplace add OrcaQubits/agentic-commerce-skills-plugins` | Claude Code |
| `clawhub install @ichiorca/openclaw-spree-commerce` | OpenClaw |
| `gemini extensions install https://github.com/OrcaQubits/agentic-commerce-skills-plugins` | Gemini CLI |
| `codex plugin marketplace add OrcaQubits/agentic-commerce-skills-plugins` | Codex CLI |
| `npx skills add orcaqubits/agentic-commerce-skills-plugins` | skills.sh — 56+ agents |
| Cursor → Settings → Plugins → Team Marketplaces → Import the GitHub URL | Cursor Teams |

**A single repo, six install paths, ~290 skills, 0 vendor-gated reviews completed yet.**

---

## Strategic recommendation

The auto-aggregator and topic-driven catalogs do 80% of the discoverability work for free. The form-based catalogs are one-evening user actions when you're ready. The vendor-gated catalogs (Anthropic-official, Cursor-public) are blocked by authorship policy and aren't worth retrying without a vendor partnership.

**Highest-leverage open action**: submit to **ClaudePluginHub** (one form, auto-feeds Augment Code's discovery) and **buildwithclaude.com** (one PR, explicit multi-vendor positioning) — those two cover the major gaps left after the Tier 1-3 items.

---

## Reference URLs

- Own marketplace: https://github.com/OrcaQubits/agentic-commerce-skills-plugins
- ClawHub: https://docs.openclaw.ai/clawhub
- Gemini Gallery: https://geminicli.com/extensions/
- Cursor docs: https://cursor.com/docs/plugins
- Codex docs: https://developers.openai.com/codex/plugins
- skills.sh: https://skills.sh
- officialskills.sh: https://officialskills.sh
- buildwithclaude.com: https://buildwithclaude.com
- claudepluginhub.com: https://www.claudepluginhub.com
- claudemarketplaces.com: https://claudemarketplaces.com
- cursor.directory: https://cursor.directory
- block/agent-skills: https://github.com/block/agent-skills
- huggingface/skills: https://github.com/huggingface/skills
- agentskill.sh: https://agentskill.sh
- agensi.io: https://agensi.io
- official MCP registry: https://registry.modelcontextprotocol.io
- punkpeye/awesome-mcp-servers: https://github.com/punkpeye/awesome-mcp-servers
