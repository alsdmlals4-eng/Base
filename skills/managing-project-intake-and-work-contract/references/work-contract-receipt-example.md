# Executable Work Contract Receipt Example

Read when authoring or validating an L1+ root receipt. This fixture is not an approved task, a current project SHA, or a second status owner. Replace its sample values with fresh-read evidence and all required work for the approved Goal. Keep the execution and trust gates in the parent Skill.

WORK_CONTRACT_RECEIPT_ROOT_JSON_EXAMPLE

```json
{
  "work_level": "L1",
  "benchmark_preflight_receipt": {
    "state": "PASS",
    "entries": [
      {
        "source_and_evidence": "exact repository SHA and directly relevant approved benchmark",
        "observed_pattern": "observed owner-to-consumer boundary",
        "project_fit_and_difference": "reuse the boundary without copying project-specific values or presentation",
        "disposition": "ADAPT"
      }
    ]
  },
  "context_configuration_hygiene": {
    "scope": "only current task paths and their direct consumers",
    "inventory": [
      {
        "path": "repository-relative current owner path",
        "classification": "ACTIVE_OWNER",
        "owner_or_provenance": "verified current repository owner",
        "references_and_consumers": "direct consumer/readback checked",
        "removal_proposed": false
      }
    ]
  },
  "project_work_kanban": {
    "goal_or_slice_issue_ref": "existing approved Goal locator",
    "source_main_sha": "0123456789abcdef0123456789abcdef01234567",
    "work_item_refs": ["TASK-01"],
    "active_work_item_ref": "TASK-01",
    "next_action": "perform the next approved task",
    "work_items": [
      {
        "work_item_id": "TASK-01",
        "title": "observable approved outcome",
        "status": "IN_PROGRESS",
        "canon_owner": "repository-relative canonical owner",
        "actual_consumers": ["actual project consumer"],
        "depends_on": [],
        "acceptance_criteria": ["AC-01"],
        "required_evidence": ["E2_TEST"],
        "checklist": [
          {
            "id": "AC-01",
            "text": "condition, action, and expected result",
            "status": "NOT_RUN"
          }
        ],
        "verification": [
          {
            "level": "E2_TEST",
            "status": "NOT_RUN",
            "evidence": []
          }
        ],
        "next_action": "run the first approved implementation or verification step"
      }
    ]
  }
}
```
