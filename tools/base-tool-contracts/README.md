# Base Tool Contracts

Single shared runtime contracts for localhost Studios and the future Tool Hub.

- `ProjectFigmaRegistry` is the only Figma target-registry parser. Static entries prove `ROUTING_CONFIGURED`, not live Figma node existence or upload.
- `ApprovedAnchorRegistry` verifies a project-owned source path, exact Figma node URL, source SHA-256, approval state and evidence timestamp. Browser request fields never grant approval.
- `create_verified_run_directories` confines outputs to a project-owned, effectively gitignored `.asset-vault/library/generated/...` path and rejects tracked/protected/symlink paths.
- This package never executes project adapter `validators` or arbitrary commands.

Run its tests independently:

```bash
PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest tools/base-tool-contracts/tests -q
```
