from pathlib import Path

import pytest

from sprite_animation_studio import app


def test_cli_accepts_an_explicit_loopback_port() -> None:
    args = app.build_parser().parse_args(
        [
            "--project-root",
            str(Path("project")),
            "--fake-engine",
            "--project-id",
            "demo",
            "--port",
            "9102",
        ]
    )

    assert args.port == 9102


def test_port_zero_requires_a_private_startup_file() -> None:
    with pytest.raises(SystemExit):
        app.parse_cli_args(
            ["--project-root", "project", "--project-id", "demo", "--port", "0"]
        )


def test_hub_nonce_is_not_a_command_line_option() -> None:
    with pytest.raises(SystemExit):
        app.parse_cli_args(
            ["--project-root", "project", "--project-id", "demo", "--launch-nonce", "secret"]
        )
