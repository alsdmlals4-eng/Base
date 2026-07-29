# Base v9.0.0-rc.1 Design

## Purpose and boundary

Base v9 makes the shared operating system observable and repeatable without
turning a fixed Skill count into policy. The Registry and Skill frontmatter are
the authority; generated views make that authority visible to people, plugins,
and project adapters.

This RC changes Base only. A Base Adapter routes shared Skills into a project;
project-specific Skills, gameplay canon, code, assets, and Sheets remain in each
project. The common project adoption wave is held until separately authorized.

## Authority model

```text
SKILL_REGISTRY.json + SKILL.md frontmatter
  -> deterministic generator
  -> Base lock / plugin manifest / active-skill summary / project snapshot
  -> project Base Adapter
  -> project-specific Skill Registry and canonical sources
```

- `skills/SKILL_REGISTRY.json`: active routing records and trigger contracts.
- `SKILL.md` frontmatter: Skill identity and concise discovery description.
- Generated artifacts: read-only derivatives with hashes and provenance.
- Project adapters: select Base responsibilities without copying shared Skill
  bodies into projects.

## Contract projection

For every active Registry entry, the generator emits positive trigger, negative
trigger, owner, input, output, failure, verification, and next step. The
projection prevents an active Skill from becoming a selectable name with no
operational boundary. It does not replace the detailed Skill body.

## Google Sheets boundary

Project Sheets remain `USER_FACING_GDD_WORKSPACE` and sheet-only edits remain
`PROPOSED_SHEET_CHANGE`. Base itself is `BASE_EXCLUDED`. This RC neither reads nor
writes an external Sheet.

## UX/UI boundary

UI references may include open-source templates and demos only after licensing,
maintenance, dependency removal, non-copying, Godot transformation, and runtime
validation are recorded. Godot UI retains `Control`, `Container`, `Theme`,
`Signal`, and authoritative-state separation.
