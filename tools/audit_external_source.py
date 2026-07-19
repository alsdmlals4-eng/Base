#!/usr/bin/env python3
"""Create a deterministic, read-only inventory for an external Git repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath


SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".gd", ".go", ".h", ".hpp",
    ".html", ".java", ".js", ".jsx", ".lua", ".mjs", ".php", ".py",
    ".rb", ".rs", ".scss", ".sh", ".svelte", ".swift", ".ts", ".tsx",
    ".vue", ".sql",
}
ASSET_EXTENSIONS = {
    ".avif", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".mp3", ".ogg",
    ".otf", ".pdf", ".png", ".svg", ".ttf", ".wav", ".webp", ".woff",
    ".woff2",
}
GENERATED_PARTS = {"dist", "build", "coverage", "generated", ".next", ".vite"}
VENDOR_PARTS = {"vendor", "third_party", "node_modules"}
LOCK_NAMES = {
    "bun.lock", "bun.lockb", "cargo.lock", "composer.lock", "gemfile.lock",
    "package-lock.json", "pnpm-lock.yaml", "poetry.lock", "uv.lock", "yarn.lock",
}


def run_git(repository: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def classify(path_text: str) -> str:
    path = PurePosixPath(path_text)
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    suffix = path.suffix.lower()

    if parts & VENDOR_PARTS:
        return "vendor"
    if parts & GENERATED_PARTS:
        return "generated"
    if name in LOCK_NAMES or name.endswith(".lock"):
        return "lockfile"
    if ".github" in parts or "workflows" in parts:
        return "workflow"
    if "test" in parts or "tests" in parts or "__tests__" in parts or name.startswith("test_") or name.endswith(".test.ts") or name.endswith(".spec.ts"):
        return "test"
    if "schemas" in parts or "schema" in parts or name.endswith(".schema.json"):
        return "schema"
    if "skills" in parts or name == "skill.md":
        return "skill"
    if suffix in ASSET_EXTENSIONS:
        return "asset"
    if suffix in SOURCE_EXTENSIONS:
        return "source"
    if suffix in {".md", ".mdx", ".rst", ".txt"} or name in {"license", "license.md", "readme"}:
        return "documentation"
    if suffix in {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg", ".conf", ".env"} or name.startswith("."):
        return "configuration"
    if name == "py.typed":
        return "configuration"
    if suffix in {".ps1", ".bat", ".cmd"}:
        return "script"
    return "other"


def is_binary(data: bytes) -> bool:
    return b"\0" in data[:8192]


def inventory(repository: Path, source_name: str, source_url: str) -> dict[str, object]:
    repository = repository.resolve()
    commit = run_git(repository, "rev-parse", "HEAD").decode("ascii").strip()
    branch = run_git(repository, "rev-parse", "--abbrev-ref", "HEAD").decode("utf-8").strip()
    tracked = [
        item.decode("utf-8", errors="surrogateescape")
        for item in run_git(repository, "ls-files", "-z").split(b"\0")
        if item
    ]
    files: list[dict[str, object]] = []
    roles: Counter[str] = Counter()
    total_bytes = 0

    for relative in sorted(tracked):
        data = run_git(repository, "show", f"HEAD:{relative}")
        role = classify(relative)
        roles[role] += 1
        total_bytes += len(data)
        files.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "role": role,
                "content_kind": "binary" if is_binary(data) else "text",
                "media_type": mimetypes.guess_type(relative)[0] or "application/octet-stream",
            }
        )

    return {
        "schema_version": 1,
        "source_name": source_name,
        "source_url": source_url,
        "commit": commit,
        "branch_at_audit": branch,
        "tracked_file_count": len(files),
        "total_bytes": total_bytes,
        "role_counts": dict(sorted(roles.items())),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    payload = inventory(args.repository, args.source_name, args.source_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Inventoried {payload['tracked_file_count']} tracked files at {payload['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
