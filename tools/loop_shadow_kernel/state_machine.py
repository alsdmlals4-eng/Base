from __future__ import annotations

from dataclasses import dataclass, field

from .models import RunState


class IllegalTransition(RuntimeError):
    pass


class TransitionBudgetExceeded(RuntimeError):
    pass


_ALLOWED: dict[RunState, RunState] = {
    RunState.CREATED: RunState.PREFLIGHT,
    RunState.PREFLIGHT: RunState.AUTHORITY_SYNCED,
    RunState.AUTHORITY_SYNCED: RunState.CONTRACT_VALIDATED,
    RunState.CONTRACT_VALIDATED: RunState.COVERAGE_INITIALIZED,
    RunState.COVERAGE_INITIALIZED: RunState.LEASE_ACQUIRED,
    RunState.LEASE_ACQUIRED: RunState.SHADOW_RUNNING,
    RunState.SHADOW_RUNNING: RunState.SHADOW_VERIFIED,
    RunState.SHADOW_VERIFIED: RunState.ADVERSARIAL_REVIEWED,
    RunState.ADVERSARIAL_REVIEWED: RunState.SHADOW_COMPLETE,
}

HAPPY_PATH: tuple[RunState, ...] = tuple(_ALLOWED.values())
REQUIRED_TRANSITIONS = len(HAPPY_PATH)


@dataclass(slots=True)
class StateMachine:
    max_transitions: int = 64
    state: RunState = RunState.CREATED
    _history: list[RunState] = field(default_factory=lambda: [RunState.CREATED])

    @property
    def history(self) -> tuple[str, ...]:
        return tuple(state.value for state in self._history)

    def advance(self, target: RunState) -> RunState:
        expected = _ALLOWED.get(self.state)
        if expected is None or target is not expected:
            raise IllegalTransition(f"illegal transition {self.state.value} -> {target.value}")
        if len(self._history) - 1 >= self.max_transitions:
            raise TransitionBudgetExceeded(
                f"transition budget {self.max_transitions} exhausted before {target.value}"
            )
        self.state = target
        self._history.append(target)
        return self.state
