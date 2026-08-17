"""Browser-owned lifecycle for the localhost Tool Hub."""

from __future__ import annotations

from collections.abc import Callable
import logging
import threading
import time
from typing import Protocol


_LOGGER = logging.getLogger(__name__)


class TimerHandle(Protocol):
    daemon: bool

    def start(self) -> None: ...

    def cancel(self) -> None: ...


TimerFactory = Callable[[float, Callable[[], None]], TimerHandle]


class BrowserLeaseManager:
    """Track Tool Hub browser-page owners and request shutdown when none remain."""

    def __init__(
        self,
        shutdown_callback: Callable[[], None],
        *,
        clock: Callable[[], float] = time.monotonic,
        timer_factory: TimerFactory = threading.Timer,
        heartbeat_ttl: float = 300.0,
        shutdown_grace: float = 2.0,
    ) -> None:
        if shutdown_grace <= 0 or heartbeat_ttl <= shutdown_grace:
            raise ValueError("browser lease timing is invalid")
        self._shutdown_callback = shutdown_callback
        self._clock = clock
        self._timer_factory = timer_factory
        self._heartbeat_ttl = float(heartbeat_ttl)
        self._shutdown_grace = float(shutdown_grace)
        self._leases: dict[str, float] = {}
        self._armed = False
        self._zero_since: float | None = None
        self._shutdown_requested = False
        self._stopped = False
        self._timer: TimerHandle | None = None
        self._lock = threading.RLock()

    @property
    def armed(self) -> bool:
        with self._lock:
            return self._armed

    @property
    def live_count(self) -> int:
        with self._lock:
            return len(self._leases)

    def open(self, lease_id: str) -> None:
        self._touch(lease_id)

    def heartbeat(self, lease_id: str) -> None:
        self._touch(lease_id)

    def close(self, lease_id: str) -> None:
        should_shutdown = False
        with self._lock:
            if self._stopped or self._shutdown_requested or lease_id not in self._leases:
                return
            self._leases.pop(lease_id, None)
            now = self._clock()
            if not self._leases and self._armed and self._zero_since is None:
                self._zero_since = now
            should_shutdown = self._schedule_for_state_locked(now)
        if should_shutdown:
            self._request_shutdown()

    def stop(self) -> None:
        with self._lock:
            self._stopped = True
            self._cancel_timer_locked()
            self._leases.clear()
            self._zero_since = None

    def _touch(self, lease_id: str) -> None:
        should_shutdown = False
        with self._lock:
            if self._stopped or self._shutdown_requested:
                return
            now = self._clock()
            self._leases[lease_id] = now
            self._armed = True
            self._zero_since = None
            should_shutdown = self._schedule_for_state_locked(now)
        if should_shutdown:
            self._request_shutdown()

    def _cancel_timer_locked(self) -> None:
        timer = self._timer
        self._timer = None
        if timer is not None:
            timer.cancel()

    def _schedule_timer_locked(self, delay: float) -> None:
        self._cancel_timer_locked()
        timer = self._timer_factory(max(0.0, delay), self._on_timer)
        try:
            timer.daemon = True
        except (AttributeError, RuntimeError):
            pass
        self._timer = timer
        timer.start()

    def _schedule_for_state_locked(self, now: float) -> bool:
        if self._stopped or self._shutdown_requested:
            self._cancel_timer_locked()
            return False

        if self._leases:
            self._zero_since = None
            earliest_expiry = min(
                last_seen + self._heartbeat_ttl for last_seen in self._leases.values()
            )
            self._schedule_timer_locked(max(0.0, earliest_expiry - now))
            return False

        if not self._armed:
            self._cancel_timer_locked()
            return False

        if self._zero_since is None:
            self._zero_since = now
        remaining = self._shutdown_grace - (now - self._zero_since)
        if remaining > 0:
            self._schedule_timer_locked(remaining)
            return False

        self._cancel_timer_locked()
        self._shutdown_requested = True
        return True

    def _on_timer(self) -> None:
        should_shutdown = False
        with self._lock:
            if self._stopped or self._shutdown_requested:
                return
            self._timer = None
            now = self._clock()
            stale = [
                lease_id
                for lease_id, last_seen in self._leases.items()
                if now - last_seen >= self._heartbeat_ttl
            ]
            for lease_id in stale:
                self._leases.pop(lease_id, None)
            if stale and not self._leases and self._armed and self._zero_since is None:
                self._zero_since = now
            should_shutdown = self._schedule_for_state_locked(now)
        if should_shutdown:
            self._request_shutdown()

    def _request_shutdown(self) -> None:
        try:
            self._shutdown_callback()
        except Exception:
            _LOGGER.exception("browser lease shutdown callback failed")
