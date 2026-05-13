#!/usr/bin/env python3
"""PreToolUse hook: block potentially destructive Rails / Spree / database commands."""
import json, sys, re

# Commands that can cause data loss or production outage — BLOCK these
DESTRUCTIVE_PATTERNS = [
    (r'(rails|rake|bin/rails)\s+db:drop', "rails db:drop — drops the database (permanent data loss)"),
    (r'(rails|rake|bin/rails)\s+db:reset', "rails db:reset — drops and recreates the database"),
    (r'(rails|rake|bin/rails)\s+db:migrate:reset', "rails db:migrate:reset — drops and re-migrates the database"),
    (r'(rails|rake|bin/rails)\s+db:purge', "rails db:purge — wipes all data from the database"),
    (r'(rails|rake|bin/rails)\s+spree_sample:load.*--force', "spree_sample:load --force — overwrites existing data"),
    (r'DROP\s+(TABLE|DATABASE|SCHEMA)', "SQL DROP statement — permanent data loss"),
    (r'TRUNCATE\s+TABLE', "SQL TRUNCATE — deletes all table data"),
    (r'rm\s+(-rf?|.*-r)\s+.*(public/uploads|storage|tmp/cache)', "Removing Rails storage / uploads — irrecoverable"),
    (r'docker[-\s]compose\s+.*down\s+.*-v', "docker compose down -v — destroys persistent volumes"),
    (r'rails\s+destroy\s+spree:install', "rails destroy spree:install — removes Spree installation"),
]

# Commands that should warn but allow
WARNING_PATTERNS = [
    (r'(rails|rake|bin/rails)\s+db:migrate', "rails db:migrate — will modify the database schema"),
    (r'(rails|rake|bin/rails)\s+db:rollback', "rails db:rollback — reverts the last migration"),
    (r'(rails|rake|bin/rails)\s+db:seed', "rails db:seed — runs seed data scripts"),
    (r'(rails|rake|bin/rails)\s+spree_sample:load', "spree_sample:load — loads Spree sample data"),
    (r'(rails|rake|bin/rails)\s+spree:install', "spree:install — initializes Spree in this app"),
    (r'(rails|rake|bin/rails)\s+assets:precompile', "assets:precompile — precompiles Tailwind/JS assets"),
    (r'sidekiq\s+', "Starting Sidekiq — background job worker"),
    (r'bundle\s+exec\s+rspec', "Running RSpec test suite"),
    (r'heroku\s+(run|releases:rollback|maintenance)', "Heroku production action — verify environment"),
    (r'docker[-\s]compose\s+.*up', "Starting Docker services"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        return

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only inspect commands that look like Rails / Spree / DB / Docker / Heroku ops
    lower = command.lower()
    if not any(kw in lower for kw in (
        "rails", "rake", "bundle", "spree", "sidekiq", "heroku", "docker", "drop ", "truncate "
    )):
        return

    # Block destructive patterns
    for pattern, desc in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                f"Blocked: '{command}' — {desc}. "
                "This command is potentially destructive. "
                "Please confirm with the user before running.",
                file=sys.stderr,
            )
            sys.exit(2)

    # Warn on caution patterns
    warnings = []
    for pattern, desc in WARNING_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(desc)

    if warnings:
        msg = (
            f"Spree/Rails CLI notice for '{command}': {'; '.join(warnings)}. "
            "Ensure this is intentional."
        )
        json.dump({"systemMessage": msg}, sys.stdout)


if __name__ == "__main__":
    main()
