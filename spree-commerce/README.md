# Spree Commerce Plugin for Claude Code

A deeply expert Claude Code plugin for building on **Spree Commerce** — the open-source Rails e-commerce platform created by Sean Schofield in 2007, used by Bookshop, Bonobos, GoDaddy, Huckberry, KFC, Blue Apron, the New England Patriots, and 5,000+ businesses.

## Design Philosophy

This plugin is built to **stay current**:

- **Conceptual knowledge is baked in** — architecture (the consolidated `spree` umbrella gem, Tailwind admin, Hotwire), state machines (Order/Payment/Shipment), the four customization surfaces (Events > Webhooks > Dependencies > Decorators), and patterns stable across minor releases.
- **Implementation-specific details are fetched live** — the subagent and every skill instruct Claude Code to web-search and web-fetch the official docs (spreecommerce.org/docs, GitHub releases) and the live `spree` gem source before writing code, so you always get the latest config keys, API paths, event names, generator commands, and gem versions.
- **Spree version is always cited** — generated code includes comments referencing the Spree release it was written against.

## Plugin Structure

```
spree-commerce/
├── .claude-plugin/
│   └── plugin.json                          # Plugin manifest
├── agents/
│   └── spree-expert.md                      # Subagent: full Spree expert
├── hooks/
│   ├── hooks.json                           # Lifecycle hooks configuration
│   └── scripts/
│       ├── check_spree_commands.py          # PreToolUse: block destructive Rails / Spree commands
│       └── check_secrets.py                 # PostToolUse: detect hardcoded secrets
├── skills/
│   ├── spree-setup/SKILL.md                 # create-spree-app, spree-starter, Docker
│   ├── spree-data-model/SKILL.md            # Order/Variant/Taxon/Stock/Payment graph + Markets
│   ├── spree-checkout/SKILL.md              # Order/Payment/Shipment state machines + returns
│   ├── spree-catalog/SKILL.md               # Products/Variants/Options/Taxonomies/MeiliSearch
│   ├── spree-promotions/SKILL.md            # Rules/Actions/Calculators/CouponCodes
│   ├── spree-payments/SKILL.md              # Stripe/Adyen/PayPal/PaymentSession (v5.4+)
│   ├── spree-shipping-fulfillment/SKILL.md  # ShippingMethod/Stock::Estimator/Returns
│   ├── spree-api-v3/SKILL.md                # /api/v3/ flat-JSON Store + Admin API
│   ├── spree-legacy-api-v2/SKILL.md         # JSON:API v2 + spree_legacy_api_v2 gem
│   ├── spree-typescript-sdk/SKILL.md        # @spree/sdk with Zod
│   ├── spree-events-webhooks/SKILL.md       # Spree::Events + Webhooks 2.0 HMAC
│   ├── spree-extensions/SKILL.md            # Engines + prepend decorators + Dependencies
│   ├── spree-admin-customization/SKILL.md   # Spree.admin.navigation + partial slots
│   ├── spree-multi-store/SKILL.md           # Multi-store + Markets + Marketplace
│   ├── spree-headless-storefront/SKILL.md   # Next.js 16 storefront repo
│   ├── spree-testing/SKILL.md               # RSpec + FactoryBot + spree_dev_tools
│   ├── spree-deployment/SKILL.md            # PostgreSQL/Redis/Sidekiq/Docker/Heroku
│   ├── spree-security/SKILL.md              # Devise + CanCanCan + OWASP + PCI scope
│   ├── spree-performance/SKILL.md           # N+1, caching, Sidekiq, Black Friday playbook
│   ├── spree-i18n/SKILL.md                  # spree_i18n + Translations Center (v5.4+)
│   ├── spree-upgrades/SKILL.md              # v4→v5 migration + v5.x→v5.y upgrade workflow
│   └── spree-dev-patterns/SKILL.md          # Customization hierarchy + Spree-on-Rails idioms
└── README.md
```

## Installation

### Per-session

```bash
claude --plugin-dir "spree-commerce"
```

### Persistent

Add to `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "spree-commerce": {
      "type": "local",
      "path": "/path/to/agentic-commerce-claude-plugins/spree-commerce"
    }
  }
}
```

### Verify

Run `/agents` in Claude Code — you should see `spree-commerce:spree-expert`.

## Using the Subagent

### Auto-delegation

Claude auto-delegates when your task involves Spree:

```
Build a Spree extension that syncs orders to NetSuite via the event bus
```

```
Add a custom shipping calculator to my Spree v5.4 store
```

```
Migrate my Spree v4 admin customizations to the v5 Tailwind dashboard
```

### Explicit invocation

```
Use the spree-expert subagent to debug why my Webhook 2.0 signatures are failing verification
```

### What makes it different

The subagent has `WebSearch` and `WebFetch` in its tool list. Before writing implementation code, it will:

1. Search for the latest release on github.com/spree/spree/releases
2. Fetch the relevant doc page on spreecommerce.org/docs
3. Inspect the live `spree` gem source for the current API surface
4. Write code against the verified-current release, citing the version

## Available Skills

| Skill | Invocation | Description |
|---|---|---|
| **spree-setup** | Auto + manual | Bootstrap with `create-spree-app`, spree-starter, Docker |
| **spree-data-model** | Auto + manual | Order/LineItem/Variant/Taxon/Stock graph + v5.4 Markets |
| **spree-checkout** | Auto + manual | Order/Payment/Shipment state machines + returns flow |
| **spree-catalog** | Auto + manual | Products, variants, options, taxonomies, MeiliSearch, CSV import |
| **spree-promotions** | Auto + manual | Rules/Actions/Calculators, coupon batches, advanced engine |
| **spree-payments** | Auto + manual | Stripe/Adyen/PayPal, Payment Sessions (v5.4+), custom gateways |
| **spree-shipping-fulfillment** | Auto + manual | ShippingMethod, Stock::Estimator, multi-shipment, returns |
| **spree-api-v3** | Auto + manual | `/api/v3/` flat-JSON Store API + Admin API, OpenAPI 3.0 |
| **spree-legacy-api-v2** | Auto + manual | JSON:API v2 via `spree_legacy_api_v2`, migration to v3 |
| **spree-typescript-sdk** | Auto + manual | `@spree/sdk`, Zod schemas, server-only auth |
| **spree-events-webhooks** | Auto + manual | `Spree::Events`, Subscribers, Webhooks 2.0 HMAC |
| **spree-extensions** | Auto + manual | Engine scaffolding, `prepend` decorators, `Spree::Dependencies` |
| **spree-admin-customization** | Auto + manual | `Spree.admin.navigation`, partial slots, Admin SDK |
| **spree-multi-store** | Auto + manual | Multi-store, Markets, Marketplace (Enterprise) |
| **spree-headless-storefront** | Auto + manual | Next.js 16 storefront repo customization + deploy |
| **spree-testing** | Auto + manual | RSpec, FactoryBot, Capybara, `spree_dev_tools` |
| **spree-deployment** | Auto + manual | PostgreSQL/Redis/Sidekiq/Docker on Heroku/Render/Fly/AWS |
| **spree-security** | Auto + manual | Devise + CanCanCan + OWASP + PCI scope + multi-store isolation |
| **spree-performance** | Auto + manual | N+1, caching, Sidekiq tuning, Black Friday prep |
| **spree-i18n** | Auto + manual | `spree_i18n` + Translations Center (v5.4+) + RTL |
| **spree-upgrades** | Auto + manual | v4→v5 and v5.x→v5.y upgrade workflow |
| **spree-dev-patterns** | Auto + manual | Customization hierarchy + Spree-on-Rails idioms |

## Hooks

The plugin includes lifecycle hooks that provide safety guardrails:

| Event | Trigger | Behavior |
|-------|---------|----------|
| **PreToolUse** (sync) | Bash | Blocks destructive Rails / DB commands (`rails db:drop`, `db:reset`, `db:purge`, `DROP TABLE`, `TRUNCATE`, `docker compose down -v`); warns on `db:migrate` / `db:rollback` / `db:seed` / `spree_sample:load`. |
| **PostToolUse** (async) | Write or Edit | Scans written code for hardcoded Rails `SECRET_KEY_BASE`, Stripe (`sk_live_`, `whsec_`), Adyen, PayPal, Klaviyo, AWS, GitHub tokens, OAuth client secrets, Postgres/MySQL URLs with embedded passwords, and PEM private keys. |

Hooks require Python in PATH.

## Spree at a Glance

### v5 Stack

| Layer | Tech |
|-------|------|
| Framework | Rails 7+ |
| Admin UI | Tailwind 4 + Hotwire (Turbo + Stimulus) |
| Backend gem | `spree` umbrella (was many engines pre-v5) |
| Storefront | Next.js 16 (`spree/storefront`) or Rails (`spree-rails-storefront`) |
| API generations | v3 (flat JSON, OpenAPI 3.0, recommended) + v2 (JSON:API via `spree_legacy_api_v2`) |
| Background jobs | Sidekiq + Redis |
| DB | PostgreSQL 14+ |
| Search | MeiliSearch (v5.4+ default) |

### Customization Hierarchy

```
1. Event Subscribers      ← lowest coupling, upgrade-safe
2. Webhooks 2.0
3. Spree::Dependencies (service swap)
4. Admin Navigation + Partial Slots
5. Decorators (prepend)   ← highest coupling, upgrade-fragile
```

Always reach for the lowest-numbered tool that solves your problem.

### Order State Machine

```
cart → address → delivery → payment → confirm → complete
```

### Five Top-Level Domains

| Domain | Models |
|--------|--------|
| **Catalog** | Product, Variant, OptionType, Taxonomy, Image, Metafield |
| **Order graph** | Order, LineItem, Adjustment, Shipment, Payment, PaymentSession (v5.4+) |
| **Inventory** | StockLocation, StockItem, StockMovement |
| **Identity** | User, Role, Address, StoreCredit, GiftCard |
| **Multi-store** | Store, Market (v5.4+), Theme, CmsPage |

## Official References

| Resource | URL |
|----------|-----|
| Marketing site | https://spreecommerce.org |
| Docs | https://spreecommerce.org/docs/ |
| Main repo | https://github.com/spree/spree |
| Releases | https://github.com/spree/spree/releases |
| spree-starter (Rails backend) | https://github.com/spree/spree-starter |
| Next.js storefront | https://github.com/spree/storefront |
| Stripe integration | https://github.com/spree/spree_stripe |
| Adyen integration | https://github.com/spree/spree_adyen |
| PayPal integration | https://github.com/spree/spree_paypal_checkout |
| Legacy v2 API gem | https://github.com/spree/spree_legacy_api_v2 |
| i18n gem | https://github.com/spree-contrib/spree_i18n |
| v5.0 announcement | https://spreecommerce.org/announcing-spree-5-the-biggest-open-source-release-ever/ |
| v5.2 announcement | https://spreecommerce.org/announcing-spree-5-2/ |
| v5.4 announcement | https://spreecommerce.org/announcing-spree-commerce-5-4/ |

## Used By

Per spreecommerce.org: Bookshop, Bonobos, GoDaddy, Huckberry, KFC, Blue Apron, Garmentory, Maisonette, Marley Spoon, Packhelp, the New England Patriots, and 5,000+ businesses.

## License

MIT (this plugin). Spree itself is BSD-3-Clause.
