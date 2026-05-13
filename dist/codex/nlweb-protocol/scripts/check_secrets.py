#!/usr/bin/env python3
"""PostToolUse hook: detect hardcoded LLM / vector-store / cloud secrets in NLWeb code."""
import json, sys, re

PATTERNS = [
    (r'sk-[a-zA-Z0-9]{32,}', "OpenAI / Anthropic style API key (sk-)"),
    (r'sk-ant-[a-zA-Z0-9_\-]{32,}', "Anthropic API key (sk-ant-)"),
    (r'AZURE_OPENAI_API_KEY\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded AZURE_OPENAI_API_KEY"),
    (r'AZURE_SEARCH_API_KEY\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded AZURE_SEARCH_API_KEY"),
    (r'AIza[0-9A-Za-z_\-]{30,}', "Google / Gemini API key (AIza)"),
    (r'qdrant[_-]?api[_-]?key\s*[:=]\s*["\'][^"\']{16,}["\']', "Hardcoded Qdrant API key"),
    (r'SNOWFLAKE_PASSWORD\s*=\s*["\'][^"\']+["\']', "Hardcoded Snowflake password"),
    (r'SNOWFLAKE_PRIVATE_KEY\s*=\s*["\'][^"\']+["\']', "Hardcoded Snowflake private key"),
    (r'HF_TOKEN\s*=\s*["\']hf_[^"\']+["\']', "Hardcoded HuggingFace token"),
    (r'CLOUDFLARE_API_TOKEN\s*=\s*["\'][^"\']{20,}["\']', "Hardcoded Cloudflare API token"),
    (r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----', "Private key material"),
    (r'BING_SEARCH_KEY\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded Bing Search key"),
]

SKIP_EXTENSIONS = {".md", ".txt", ".rst", ".csv", ".svg", ".png", ".jpg", ".gif"}


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "")
    else:
        return

    file_path = tool_input.get("file_path", "")
    if any(file_path.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
        return

    warnings = []
    for pattern, desc in PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(desc)

    if warnings:
        msg = (
            f"Security notice: Possible hardcoded secret(s) detected in {file_path}: "
            f"{', '.join(warnings)}. NLWeb expects credentials via .env / environment variables, "
            f"not hardcoded in config_*.yaml or source."
        )
        json.dump({"systemMessage": msg}, sys.stdout)


if __name__ == "__main__":
    main()
