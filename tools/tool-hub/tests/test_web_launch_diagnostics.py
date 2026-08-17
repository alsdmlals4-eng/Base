from pathlib import Path

from fastapi.testclient import TestClient

from tool_hub.app import create_app
from tool_hub.browser_lifecycle import BrowserLeaseManager


ROOT = Path(__file__).resolve().parents[3]
APP_JS = ROOT / "tools" / "tool-hub" / "web" / "app.js"
VALID_LEASE_A = "11111111-1111-4111-8111-111111111111"
VALID_LEASE_B = "22222222-2222-4222-8222-222222222222"
VALID_LEASE_C = "33333333-3333-4333-8333-333333333333"


class ManualClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


class ManualTimer:
    def __init__(self, delay: float, callback) -> None:
        self.delay = delay
        self.callback = callback
        self.cancelled = False
        self.daemon = False

    def start(self) -> None:
        return None

    def cancel(self) -> None:
        self.cancelled = True

    def fire(self) -> None:
        if not self.cancelled:
            self.callback()


class TimerHarness:
    def __init__(self) -> None:
        self.timers: list[ManualTimer] = []

    def __call__(self, delay: float, callback) -> ManualTimer:
        timer = ManualTimer(delay, callback)
        self.timers.append(timer)
        return timer

    @property
    def latest(self) -> ManualTimer:
        return self.timers[-1]


def manager_fixture():
    clock = ManualClock()
    timers = TimerHarness()
    shutdowns: list[str] = []
    manager = BrowserLeaseManager(
        lambda: shutdowns.append("shutdown"),
        clock=clock,
        timer_factory=timers,
        heartbeat_ttl=300.0,
        shutdown_grace=2.0,
    )
    return manager, clock, timers, shutdowns


def make_lease_app(tmp_path: Path, *, shutdowns: list[str] | None = None):
    observed = shutdowns if shutdowns is not None else []
    app = create_app(
        ROOT,
        tmp_path / "projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        launch_supported=False,
        shutdown_callback=lambda: observed.append("stop"),
    )
    return app, observed


def bootstrap_mutation_client(client: TestClient) -> None:
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]


def test_browser_lease_manager_waits_for_first_browser_owner() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    clock.advance(1000)

    assert manager.armed is False
    assert manager.live_count == 0
    assert timers.timers == []
    assert shutdowns == []


def test_final_explicit_close_shuts_down_after_two_second_grace() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    manager.open("lease-a")
    manager.close("lease-a")

    assert manager.armed is True
    assert manager.live_count == 0
    assert timers.latest.delay == 2.0
    clock.advance(2.0)
    timers.latest.fire()
    assert shutdowns == ["shutdown"]


def test_replacement_lease_during_grace_cancels_shutdown() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    manager.open("lease-a")
    manager.close("lease-a")
    closing_timer = timers.latest
    manager.open("lease-b")

    assert closing_timer.cancelled is True
    assert manager.live_count == 1
    clock.advance(2.0)
    closing_timer.fire()
    assert shutdowns == []


def test_one_of_two_tabs_closing_keeps_hub_alive() -> None:
    manager, _, timers, shutdowns = manager_fixture()

    manager.open("lease-a")
    manager.open("lease-b")
    manager.close("lease-a")

    assert manager.live_count == 1
    assert timers.latest.delay == 300.0
    assert shutdowns == []


def test_recent_background_heartbeat_is_not_expired() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    manager.open("lease-a")
    initial_stale_timer = timers.latest
    clock.advance(299.0)
    initial_stale_timer.fire()

    assert manager.live_count == 1
    assert shutdowns == []
    assert 0.0 < timers.latest.delay <= 1.0


def test_stale_lease_uses_300_second_crash_fallback_then_grace() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    manager.open("lease-a")
    stale_timer = timers.latest
    assert stale_timer.delay == 300.0

    clock.advance(300.0)
    stale_timer.fire()
    assert manager.live_count == 0
    assert shutdowns == []
    assert timers.latest.delay == 2.0

    clock.advance(2.0)
    timers.latest.fire()
    assert shutdowns == ["shutdown"]


def test_unknown_close_is_idempotent_and_shutdown_fires_once() -> None:
    manager, clock, timers, shutdowns = manager_fixture()

    manager.close("unknown-before-arm")
    assert shutdowns == []
    assert timers.timers == []

    manager.open("lease-a")
    manager.close("lease-a")
    grace_timer = timers.latest
    manager.close("lease-a")

    clock.advance(2.0)
    grace_timer.fire()
    grace_timer.fire()

    assert shutdowns == ["shutdown"]


def test_browser_lease_mutations_require_existing_origin_session_and_csrf(tmp_path: Path) -> None:
    app, _ = make_lease_app(tmp_path)
    with TestClient(app) as client:
        assert client.post("/api/browser-lease/open", json={"lease_id": VALID_LEASE_A}).status_code == 403

        client.headers["Origin"] = "http://testserver"
        client.get("/api/config")
        assert client.post("/api/browser-lease/open", json={"lease_id": VALID_LEASE_A}).status_code == 403


def test_browser_lease_payload_rejects_non_uuid_and_extra_fields(tmp_path: Path) -> None:
    app, _ = make_lease_app(tmp_path)
    with TestClient(app) as client:
        bootstrap_mutation_client(client)

        invalid = client.post("/api/browser-lease/open", json={"lease_id": "not-a-uuid"})
        extra = client.post(
            "/api/browser-lease/open",
            json={"lease_id": VALID_LEASE_A, "project_id": "urban-legend"},
        )

        assert invalid.status_code == 422
        assert extra.status_code == 422


def test_browser_lease_open_heartbeat_and_close_are_idempotent(tmp_path: Path) -> None:
    app, shutdowns = make_lease_app(tmp_path)
    with TestClient(app) as client:
        bootstrap_mutation_client(client)

        opened_a = client.post("/api/browser-lease/open", json={"lease_id": VALID_LEASE_A})
        opened_b = client.post("/api/browser-lease/open", json={"lease_id": VALID_LEASE_B})
        heartbeat = client.post("/api/browser-lease/heartbeat", json={"lease_id": VALID_LEASE_A})
        closed = client.post("/api/browser-lease/close", json={"lease_id": VALID_LEASE_A})
        duplicate = client.post("/api/browser-lease/close", json={"lease_id": VALID_LEASE_A})
        unknown = client.post("/api/browser-lease/close", json={"lease_id": VALID_LEASE_C})

        assert opened_a.json() == {"state": "OPEN"}
        assert opened_b.json() == {"state": "OPEN"}
        assert heartbeat.json() == {"state": "ALIVE"}
        assert closed.json() == {"state": "CLOSED"}
        assert duplicate.json() == {"state": "CLOSED"}
        assert unknown.json() == {"state": "CLOSED"}
        assert app.state.browser_leases.live_count == 1
        assert shutdowns == []


def test_explicit_shutdown_still_uses_immediate_reviewed_shutdown_path(tmp_path: Path) -> None:
    shutdowns: list[str] = []
    app, _ = make_lease_app(tmp_path, shutdowns=shutdowns)
    with TestClient(app) as client:
        bootstrap_mutation_client(client)
        assert client.post("/api/browser-lease/open", json={"lease_id": VALID_LEASE_A}).status_code == 200

        shutdown = client.post("/api/shutdown", json={})

        assert shutdown.status_code == 200
        assert shutdown.json() == {"state": "SHUTTING_DOWN"}
        assert shutdowns == ["stop"]


def test_launch_failure_keeps_the_exact_server_error_visible() -> None:
    source = APP_JS.read_text(encoding="utf-8")

    assert 'status: "START_FAILED"' in source
    assert 'detail: message' in source
    assert 'show(`${tool.display_name} 시작 차단: ${error.message}`, true);' in source
