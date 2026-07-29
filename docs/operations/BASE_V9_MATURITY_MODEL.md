# Base v9 Operating-System Maturity Model

## Use the minimum sufficient level

This model is a planning and audit aid, not a mandate to make every project reach
the highest level. Select the lowest level that protects the project's 규모,
change 위험, player impact, and reversibility. A small, isolated change can remain
at a lower level when its contract and evidence are adequate; a risky change may
need a higher level even in a small project.

Level 0~5는 프로젝트에 일률적으로 강제하지 않는다. 현재 규모와 위험에
비례해 필요한 최소 수준만 선택한다.

| Level | Capability | Minimum operating evidence | Typical use |
| --- | --- | --- | --- |
| Level 0 | Ad hoc | User instruction and a visible result; no claim of durable operational control | Disposable exploration or a one-off draft |
| Level 1 | Traceable | One canonical task description, scope, and completion check | Small bounded documentation or implementation change |
| Level 2 | Contracted | PLAN→BUILD→REVIEW path, ownership, acceptance criteria, and relevant tests | Multi-file change or a stable gameplay/system decision |
| Level 3 | Governed | Canonical map, change propagation, decision records, and adversarial review where risk warrants it | Shared systems, release slices, or persistent player data |
| Level 4 | Measured | Reproducible evidence, runtime/UX checks, freshness and regression controls | Release candidate or high-impact cross-discipline work |
| Level 5 | Learning | Level 4 plus evidence-backed reusable lessons, migration control, and improvement feedback loops | Mature Base patterns and repeatable multi-project practices |

## Assessment rule

Record the selected level, why it is sufficient for the current 규모 and 위험,
and the evidence that supports it. Do not infer maturity from document volume,
a Skill count, or a passing workflow alone.
