from __future__ import annotations

import base64
import json
import os
import pathlib
import subprocess
import tempfile
import urllib.request

REPO = os.environ["GH_REPOSITORY"]
TOKEN = os.environ["GH_TOKEN"]
TEMP_PATHS = {
    ".github/workflows/resolve-pr66-merge.yml",
    ".github/workflows/resolve-pr66-merge-run.yml",
    "tools/resolve_pr66_merge.py",
    "tmp/pr66-merge-trigger.txt",
}
JSON_CONFLICTS = {
    ".github/reference-freshness.json",
    "skills/SKILL_REGISTRY.json",
}


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout.strip()


def show(ref: str, path: str) -> str:
    return git("show", f"{ref}:{path}")


MISSING = object()


def keyed_list(values: list) -> str | None:
    if not values or not all(isinstance(item, dict) for item in values):
        return None
    for candidate in ("skill_id", "name", "source_id", "id"):
        if all(candidate in item for item in values):
            keys = [item[candidate] for item in values]
            if len(keys) == len(set(keys)):
                return candidate
    return None


def merge3(base, ours, theirs, path: str = "root"):
    if ours == theirs:
        return ours
    if ours == base:
        return theirs
    if theirs == base:
        return ours

    if all(isinstance(value, dict) for value in (base, ours, theirs)):
        result = {}
        keys = list(dict.fromkeys([*base.keys(), *ours.keys(), *theirs.keys()]))
        for key in keys:
            b = base.get(key, MISSING)
            o = ours.get(key, MISSING)
            t = theirs.get(key, MISSING)
            if o is MISSING and t is MISSING:
                continue
            if b is MISSING:
                if o is MISSING:
                    result[key] = t
                elif t is MISSING or o == t:
                    result[key] = o
                else:
                    result[key] = merge3({}, o, t, f"{path}.{key}")
                continue
            if o is MISSING:
                if t == b:
                    continue
                result[key] = t
                continue
            if t is MISSING:
                if o == b:
                    continue
                result[key] = o
                continue
            result[key] = merge3(b, o, t, f"{path}.{key}")
        return result

    if all(isinstance(value, list) for value in (base, ours, theirs)):
        combined = [*base, *ours, *theirs]
        key = keyed_list(combined)
        if key:
            b_map = {item[key]: item for item in base}
            o_map = {item[key]: item for item in ours}
            t_map = {item[key]: item for item in theirs}
            order = []
            for source in (ours, theirs, base):
                for item in source:
                    if item[key] not in order:
                        order.append(item[key])
            result = []
            for item_key in order:
                b = b_map.get(item_key, MISSING)
                o = o_map.get(item_key, MISSING)
                t = t_map.get(item_key, MISSING)
                if b is MISSING:
                    if o is MISSING:
                        result.append(t)
                    elif t is MISSING or o == t:
                        result.append(o)
                    else:
                        result.append(merge3({}, o, t, f"{path}[{item_key!r}]"))
                elif o is MISSING:
                    if t != b:
                        result.append(t)
                elif t is MISSING:
                    if o != b:
                        result.append(o)
                else:
                    result.append(merge3(b, o, t, f"{path}[{item_key!r}]"))
            return result

        result = []
        for item in [*ours, *theirs]:
            if item not in result:
                result.append(item)
        return result

    raise RuntimeError(
        f"Unresolved scalar/type conflict at {path}: "
        f"base={base!r}, ours={ours!r}, theirs={theirs!r}"
    )


def resolve_markdown_union(base_ref: str, ours_ref: str, theirs_ref: str, path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = pathlib.Path(temp_dir)
        ours_file = temp / "ours"
        base_file = temp / "base"
        theirs_file = temp / "theirs"
        ours_file.write_text(show(ours_ref, path) + "\n", encoding="utf-8")
        base_file.write_text(show(base_ref, path) + "\n", encoding="utf-8")
        theirs_file.write_text(show(theirs_ref, path) + "\n", encoding="utf-8")
        result = subprocess.run(
            [
                "git",
                "merge-file",
                "-p",
                "--union",
                str(ours_file),
                str(base_file),
                str(theirs_file),
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        pathlib.Path(path).write_text(result.stdout, encoding="utf-8")


def api(method: str, endpoint: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("fetch", "origin", "main")

    ours = git("rev-parse", "HEAD")
    theirs = git("rev-parse", "origin/main")
    base = git("merge-base", ours, theirs)
    print(f"OURS={ours}")
    print(f"THEIRS={theirs}")
    print(f"BASE={base}")

    merge = subprocess.run(
        ["git", "merge", "--no-commit", "--no-ff", theirs],
        check=False,
        text=True,
    )
    if merge.returncode not in (0, 1):
        raise RuntimeError(f"git merge failed with status {merge.returncode}")

    conflicts = [
        line
        for line in git("diff", "--name-only", "--diff-filter=U", check=False).splitlines()
        if line
    ]
    print("CONFLICTS=" + json.dumps(conflicts, ensure_ascii=False))

    for path in conflicts:
        if path in JSON_CONFLICTS:
            merged = merge3(
                json.loads(show(base, path)),
                json.loads(show(ours, path)),
                json.loads(show(theirs, path)),
                path,
            )
            pathlib.Path(path).write_text(
                json.dumps(merged, ensure_ascii=False, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
        elif path.endswith(".md"):
            resolve_markdown_union(base, ours, theirs, path)
        else:
            raise RuntimeError(f"Unexpected unresolved path: {path}")
        git("add", "--", path)

    remaining = git("diff", "--name-only", "--diff-filter=U", check=False)
    if remaining:
        raise RuntimeError(f"Unresolved paths remain:\n{remaining}")

    for path in sorted(TEMP_PATHS):
        if pathlib.Path(path).exists():
            git("rm", "--", path)

    git("add", "-A")
    git("diff", "--cached", "--check")

    changed = git("diff", "--cached", "--name-status", ours).splitlines()
    tree_entries = []
    for row in changed:
        if not row:
            continue
        parts = row.split("\t")
        status = parts[0]
        path = parts[-1]
        if status.startswith("D"):
            old = git("ls-tree", ours, "--", path)
            old_mode = old.split()[0] if old else "100644"
            tree_entries.append(
                {"path": path, "mode": old_mode, "type": "blob", "sha": None}
            )
            continue

        stage = git("ls-files", "-s", "--", path)
        if not stage:
            raise RuntimeError(f"Cannot determine index mode for {path}")
        mode = stage.split()[0]
        content = pathlib.Path(path).read_bytes()
        blob = api(
            "POST",
            "/git/blobs",
            {
                "content": base64.b64encode(content).decode("ascii"),
                "encoding": "base64",
            },
        )
        tree_entries.append(
            {"path": path, "mode": mode, "type": "blob", "sha": blob["sha"]}
        )

    base_tree = git("rev-parse", f"{ours}^{{tree}}")
    tree = api(
        "POST",
        "/git/trees",
        {"base_tree": base_tree, "tree": tree_entries},
    )
    commit = api(
        "POST",
        "/git/commits",
        {
            "message": "chore: merge latest main into game design difficulty workflow",
            "tree": tree["sha"],
            "parents": [ours, theirs],
        },
    )
    print(f"RESOLVED_COMMIT_SHA={commit['sha']}")
    print(f"RESOLVED_TREE_SHA={tree['sha']}")


if __name__ == "__main__":
    main()
