# Open-Source Godot UI Reference Catalog

This catalog is an evaluation starting point, not an approval list. Every project
must complete `templates/research/UX_UI_REFERENCE_CARD.md` and confirm the pinned
revision, license, assets, dependencies, and Godot version before adoption.

| Candidate | Useful evidence | Initial license finding | Required project decision |
| --- | --- | --- | --- |
| [Godot demo projects](https://github.com/godotengine/godot-demo-projects) | Official examples for `Control`, layout, input, and focused interaction patterns | MIT; retain the required notice when copying substantial code | Prefer extracting a small pattern; do not convert a demo's presentation into a project UI |
| [Maaack's Game Template](https://github.com/Maaack/Godot-Game-Template) | Menu, options, pause, accessibility, keyboard/gamepad, and resolution-oriented structure | Repository identifies MIT; review `ATTRIBUTION.md` and every included asset before reuse | Trial in an isolated branch; remove unneeded autoloads, scenes, and assets before any adoption |

## Mandatory evaluation

1. Pin a commit or release and record the source URL and checked date.
2. Verify license, commercial use, attribution, modification, and redistribution
   requirements for code and for every third-party asset separately.
3. Check Godot compatibility, maintenance activity, dependency removal, security,
   and save/input coupling.
4. Transform principles into the project's `Control`/`Container`/`Theme`/`Signal`
   architecture; do not copy visual identity, text, layout composition, or assets.
5. Validate focus, keyboard/gamepad input, accessibility paths, long Korean text,
   and supported resolutions in the target project.
