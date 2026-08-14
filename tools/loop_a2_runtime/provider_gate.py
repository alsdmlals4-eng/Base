from __future__ import annotations

import subprocess
from typing import Any, Callable


_CODEX_LOGIN_STATUS_TIMEOUT_SECONDS = 10
_CHATGPT_LOGIN_STATUS = "Logged in using ChatGPT"


def paid_openai_api_gate() -> dict[str, Any]:
    return {
        "status": "NOT_PLANNED",
        "code": "PAID_OPENAI_API_FORBIDDEN",
        "message": "Separately billed OpenAI API usage is forbidden by approved Universal Loop policy.",
    }


def real_provider_gate() -> dict[str, Any]:
    """Legacy direct-API gate retained fail-closed under the approved no-paid-API policy."""
    return paid_openai_api_gate()


def subscription_codex_cli_gate(
    *,
    run_command: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> dict[str, Any]:
    """Accept only a Codex CLI session authenticated through ChatGPT."""
    runner = run_command or subprocess.run
    try:
        completed = runner(
            ["codex", "login", "status"],
            text=True,
            capture_output=True,
            timeout=_CODEX_LOGIN_STATUS_TIMEOUT_SECONDS,
            check=False,
            shell=False,
        )
    except FileNotFoundError:
        return {
            "status": "BLOCKED_UNVERIFIED",
            "code": "CODEX_CLI_UNAVAILABLE",
            "message": "Codex CLI is unavailable; no paid API fallback is allowed.",
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "BLOCKED_UNVERIFIED",
            "code": "CODEX_LOGIN_STATUS_TIMEOUT",
            "message": "Codex login status timed out; no paid API fallback is allowed.",
        }
    except OSError as exc:
        return {
            "status": "BLOCKED_UNVERIFIED",
            "code": "CODEX_LOGIN_STATUS_EXECUTION_ERROR",
            "message": f"Codex login status could not run: {type(exc).__name__}.",
        }

    if completed.returncode != 0:
        return {
            "status": "BLOCKED_UNVERIFIED",
            "code": "CODEX_LOGIN_STATUS_FAILED",
            "message": "Codex login status failed; no paid API fallback is allowed.",
        }

    if (completed.stdout or "").strip() != _CHATGPT_LOGIN_STATUS:
        return {
            "status": "BLOCKED_UNVERIFIED",
            "code": "CODEX_CHATGPT_AUTH_REQUIRED",
            "message": "Loop A2 requires Codex CLI authentication through ChatGPT; API-key authentication is not accepted.",
        }

    return {
        "status": "READY",
        "code": "CODEX_CHATGPT_AUTH_READY",
        "message": "Codex CLI is authenticated through ChatGPT; model behavior remains unverified until execution evidence exists.",
    }
