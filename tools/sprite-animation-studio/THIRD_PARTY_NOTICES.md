# Third-party notices

## `sprite-gen`

- Source: <https://github.com/aldegad/sprite-gen>
- Pinned source commit: `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`
- License: Apache License 2.0
- Role: optional, explicitly configured local generation adapter. Its source is not copied, forked, vendored, or modified by this tool.

### Upgrade and rollback

1. Record the candidate upstream commit and license in a pull request.
2. Run the fake-engine tests and a disposable project-root trial with the explicit adapter.
3. Confirm the output count, PNG validation, lineage, curation, and Godot handoff remain correct.
4. To roll back, point the local adapter configuration at the prior pinned commit and remove only the failed project-local run directory.

The Base repository never stores provider credentials, project artwork, or generated runs.
