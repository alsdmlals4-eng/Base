from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
APP_JS = ROOT / "tools" / "tool-hub" / "web" / "app.js"


def test_launch_failure_keeps_the_exact_server_error_visible() -> None:
    source = APP_JS.read_text(encoding="utf-8")

    assert 'status: "START_FAILED"' in source
    assert 'detail: message' in source
    assert 'show(`${tool.display_name} 시작 차단: ${error.message}`, true);' in source
