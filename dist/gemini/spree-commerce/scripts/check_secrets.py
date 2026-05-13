#!/usr/bin/env python3
"""AfterTool hook: detect hardcoded Rails / Spree / payment-gateway secrets in written code."""
import json, sys, re

PATTERNS = [
    # Rails / Spree
    (r'SECRET_KEY_BASE\s*[:=]\s*["\']?[a-f0-9]{32,}["\']?', "Hardcoded Rails SECRET_KEY_BASE"),
    (r'secret_key_base\s*:\s*[a-f0-9]{32,}', "Hardcoded Rails secret_key_base (credentials.yml.enc compromise)"),
    (r'SPREE_API_KEY\s*=\s*["\'][a-zA-Z0-9_\-]{20,}["\']', "Hardcoded Spree API key"),
    (r'pk_(live|test)_[a-zA-Z0-9]{16,}', "Spree/Stripe publishable key (pk_live_/pk_test_)"),
    # Payment gateways
    (r'sk_live_[a-zA-Z0-9]{20,}', "Stripe LIVE secret key (sk_live_)"),
    (r'sk_test_[a-zA-Z0-9]{20,}', "Stripe test secret key"),
    (r'rk_live_[a-zA-Z0-9]{20,}', "Stripe restricted key (rk_live_)"),
    (r'whsec_[a-zA-Z0-9]{20,}', "Stripe webhook signing secret"),
    (r'AQEyhmf[a-zA-Z0-9+/=]{20,}', "Adyen API key (AQE...)"),
    (r'(ADYEN_API_KEY|ADYEN_HMAC_KEY)\s*=\s*["\'][^"\']{20,}["\']', "Adyen API/HMAC key"),
    (r'(PAYPAL_CLIENT_SECRET|PAYPAL_SECRET)\s*=\s*["\'][^"\']{20,}["\']', "PayPal client secret"),
    (r'klaviyo_api_key\s*[:=]\s*["\']?pk_[a-zA-Z0-9]+["\']?', "Klaviyo private API key (pk_)"),
    # AWS / cloud
    (r'AKIA[0-9A-Z]{16}', "AWS access key ID (AKIA...)"),
    (r'aws_secret_access_key\s*[:=]\s*["\'][A-Za-z0-9/+=]{40}["\']', "AWS secret access key"),
    # GitHub
    (r'gh[pousr]_[A-Za-z0-9_]{36,}', "GitHub token (ghp_/gho_/ghu_/ghs_/ghr_)"),
    # Generic
    (r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----', "Private key material"),
    # OAuth / Doorkeeper
    (r'(DOORKEEPER_CLIENT_SECRET|OAUTH_CLIENT_SECRET)\s*=\s*["\'][^"\']{20,}["\']', "OAuth client secret"),
    # Database URLs with passwords
    (r'(postgres|mysql)://[^:]+:[^@\s]{8,}@', "Database URL with embedded password"),
]

SKIP_EXTENSIONS = {".md", ".txt", ".rst", ".csv", ".svg", ".png", ".jpg", ".gif", ".lock"}


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "write_file":
        content = tool_input.get("content", "")
    elif tool_name == "edit_file":
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
            f"{', '.join(warnings)}. Rails apps should use Rails credentials "
            "(`bin/rails credentials:edit`) or environment variables (`ENV['VAR']`), "
            "not hardcoded values."
        )
        json.dump({"systemMessage": msg}, sys.stdout)


if __name__ == "__main__":
    main()
