from pathlib import Path

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
