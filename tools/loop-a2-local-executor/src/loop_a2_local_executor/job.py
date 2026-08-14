from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import PurePosixPath
import re
from typing import Mapping


_SHA = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")
_RUN_ID = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:/")
_BODY = re.compile(r"\A\s*```json\r?\n(?P<payload>.+)\r?\n```\s*\Z", re.DOTALL)
_KEYS = frozenset(
    {
        "schema_version",
        "contract_role",
        "target_repository",
        "base_runtime_sha",
        "authority_sha",
        "capsule",
        "run_id",
        "provider",
    }
)


class JobContractError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


def _fail(code: str, message: str) -> JobContractError:
    return JobContractError(code, message)


def _safe_capsule(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "\x00" in value
        or _WINDOWS_DRIVE.match(value) is not None
    ):
        raise _fail("JOB_CAPSULE_INVALID", "capsule must be a closed repository-relative JSON path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise _fail("JOB_CAPSULE_INVALID", "capsule path must not escape or normalize through parent components")
    if path.suffix.casefold() != ".json" or str(path) != value:
        raise _fail("JOB_CAPSULE_INVALID", "capsule path must use canonical POSIX JSON spelling")
    return value


@dataclass(frozen=True)
class LocalA2Job:
    issue_number: int
    target_repository: str
    base_runtime_sha: str
    authority_sha: str
    capsule: str
    run_id: str
    provider: str

    @classmethod
    def from_issue(
        cls,
        issue: Mapping[str, object],
        *,
        trusted_author: str,
        required_label: str,
    ) -> "LocalA2Job":
        number = issue.get("number")
        if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
            raise _fail("JOB_ISSUE_INVALID", "issue number must be a positive integer")

        author = issue.get("author")
        if not isinstance(author, Mapping) or author.get("login") != trusted_author:
            raise _fail("UNTRUSTED_JOB_AUTHOR", "job author differs from the configured exact owner")

        labels = issue.get("labels")
        label_names: set[str] = set()
        if isinstance(labels, (list, tuple)):
            for item in labels:
                if isinstance(item, Mapping) and isinstance(item.get("name"), str):
                    label_names.add(str(item["name"]))
        if required_label not in label_names:
            raise _fail("JOB_LABEL_REQUIRED", "required local executor label is absent")

        body = issue.get("body")
        if not isinstance(body, str):
            raise _fail("JOB_BODY_INVALID", "job body must be one fenced JSON object")
        match = _BODY.fullmatch(body)
        if match is None:
            raise _fail("JOB_BODY_INVALID", "job body must contain only one json fence")
        try:
            value = json.loads(match.group("payload"))
        except json.JSONDecodeError as exc:
            raise _fail("JOB_BODY_INVALID", "job JSON could not be parsed") from exc
        if not isinstance(value, dict):
            raise _fail("JOB_BODY_INVALID", "job payload must be a JSON object")
        if set(value) != _KEYS:
            raise _fail("JOB_KEYS_INVALID", "job keys differ from the closed contract")
        if value.get("schema_version") != 1 or value.get("contract_role") != "LOOP_A2_LOCAL_JOB":
            raise _fail("JOB_IDENTITY_INVALID", "job schema/role is not LOOP_A2_LOCAL_JOB v1")
        if value.get("provider") != "real":
            raise _fail("JOB_PROVIDER_INVALID", "local unattended jobs support only the subscription-native real provider")

        base_runtime_sha = value.get("base_runtime_sha")
        authority_sha = value.get("authority_sha")
        if not isinstance(base_runtime_sha, str) or _SHA.fullmatch(base_runtime_sha) is None:
            raise _fail("JOB_SHA_INVALID", "base_runtime_sha must be lowercase 40-hex")
        if not isinstance(authority_sha, str) or _SHA.fullmatch(authority_sha) is None:
            raise _fail("JOB_SHA_INVALID", "authority_sha must be lowercase 40-hex")

        repository = value.get("target_repository")
        if not isinstance(repository, str) or _REPOSITORY.fullmatch(repository) is None:
            raise _fail("JOB_REPOSITORY_INVALID", "target_repository must be canonical owner/name")
        owner, name = repository.split("/", 1)
        if owner in {".", ".."} or name in {".", ".."} or name.casefold().endswith(".git"):
            raise _fail("JOB_REPOSITORY_INVALID", "target_repository is not canonical owner/name")

        capsule = _safe_capsule(value.get("capsule"))
        run_id = value.get("run_id")
        if not isinstance(run_id, str) or _RUN_ID.fullmatch(run_id) is None:
            raise _fail("JOB_RUN_ID_INVALID", "run_id must be 3..64 uppercase alphanumeric/_/-")

        return cls(
            issue_number=number,
            target_repository=repository,
            base_runtime_sha=base_runtime_sha,
            authority_sha=authority_sha,
            capsule=capsule,
            run_id=run_id,
            provider="real",
        )
