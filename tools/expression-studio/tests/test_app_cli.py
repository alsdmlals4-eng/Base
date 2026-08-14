from pathlib import Path

import pytest

from expression_studio import app


def required_args() -> list[str]:
    return ["--project-root", str(Path("project")), "--project-id", "demo"]


def test_cli_preserves_an_explicit_direct_operator_port() -> None:
    args = app.parse_cli_args(required_args() + ["--port", "9101"])

    assert args.port == 9101
    assert args.startup_file is None


def test_port_zero_requires_a_private_startup_file() -> None:
    with pytest.raises(SystemExit):
        app.parse_cli_args(required_args() + ["--port", "0"])


def test_hub_nonce_is_not_a_command_line_option() -> None:
    with pytest.raises(SystemExit):
        app.parse_cli_args(required_args() + ["--launch-nonce", "secret"])
