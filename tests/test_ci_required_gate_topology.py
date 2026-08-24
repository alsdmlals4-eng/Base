from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_ci_required_gate_topology.py"
VALID_CANONICAL = """name: Canonical
on:
  pull_request:
jobs:
  classify-changes:
    name: classify-changes
    runs-on: ubuntu-latest
    steps:
      - run: echo classify

  docs-validation:
    name: docs-validation
    runs-on: ubuntu-latest
    steps:
      - run: python tools/check_ci_required_gate_topology.py

  core-regression:
    name: core-regression
    runs-on: ubuntu-latest
    steps:
      - run: python -m unittest discover -s tests -v

  ubuntu-contract:
    name: ubuntu-contract
    runs-on: ubuntu-latest
    steps:
      - run: echo contract

  publication-validation:
    name: publication-validation
    runs-on: ubuntu-latest
    steps:
      - run: echo publication

  platform-smoke-windows:
    name: platform-smoke-windows
    runs-on: windows-latest
    steps:
      - run: echo windows

  ci-gate:
    name: ci-gate
    needs:
      - classify-changes
      - docs-validation
      - core-regression
      - ubuntu-contract
      - publication-validation
      - platform-smoke-windows
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1

      - name: Evaluate required validation jobs
        env:
          CLASSIFY_RESULT: ${{ needs.classify-changes.result }}
          DOCS_RESULT: ${{ needs.docs-validation.result }}
          CORE_REQUIRED: ${{ needs.classify-changes.outputs.run_core }}
          CORE_REGRESSION_RESULT: ${{ needs.core-regression.result }}
          CONTRACT_REQUIRED: ${{ needs.classify-changes.outputs.run_contract }}
          CONTRACT_RESULT: ${{ needs.ubuntu-contract.result }}
          PUBLICATION_REQUIRED: ${{ needs.classify-changes.outputs.run_publication }}
          PUBLICATION_RESULT: ${{ needs.publication-validation.result }}
          WINDOWS_REQUIRED: ${{ needs.classify-changes.outputs.run_windows }}
          WINDOWS_RESULT: ${{ needs.platform-smoke-windows.result }}
        run: python tools/evaluate_ci_required_gate.py
"""
LEGACY_FOCUSED_WORKFLOW = """name: Focused
on:
  pull_request:
    paths:
      - docs/**
jobs:
  base-v9-contract:
    name: base-v9-contract
    runs-on: ubuntu-latest
    steps:
      - run: echo contract

  ci-gate:
    name: ci-gate
    needs: base-v9-contract
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: echo gate

  adversarial-gate:
    name: adversarial-gate
    needs: [base-v9-contract, ci-gate]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: echo adversarial
"""


class CiRequiredGateTopologyTests(unittest.TestCase):
    def _run(self, workflows: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="base-ci-topology-") as temporary:
            fixture = Path(temporary)
            workflow_root = fixture / ".github/workflows"
            workflow_root.mkdir(parents=True)
            for name, body in workflows.items():
                (workflow_root / name).write_text(body, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER), "--root", str(fixture)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_single_unfiltered_canonical_gate_passes(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL,
            "focused.yml": """name: Focused
on:
  pull_request:
    paths:
      - docs/**
jobs:
  focused:
    name: focused
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
""",
        })
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CI REQUIRED GATE TOPOLOGY: PASS", result.stdout)

    def test_canonical_gate_must_checkout_before_evaluation(self) -> None:
        missing_checkout = VALID_CANONICAL.replace(
            "      - name: Check out repository\n"
            "        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n\n",
            "",
        )
        result = self._run({
            "validate-game-project-operating-system.yml": missing_checkout,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical ci-gate must checkout the repository first", result.stdout)

    def test_canonical_gate_checkout_must_use_the_pinned_action(self) -> None:
        wrong_pin = VALID_CANONICAL.replace(
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/checkout@main",
            1,
        )
        result = self._run({
            "validate-game-project-operating-system.yml": wrong_pin,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical ci-gate checkout must use the pinned action", result.stdout)

    def test_canonical_gate_checkout_must_be_unconditional_and_unmasked(self) -> None:
        variants = (
            "        if: false\n",
            "        continue-on-error: true\n",
        )
        for declaration in variants:
            with self.subTest(declaration=declaration.strip()):
                mutated = VALID_CANONICAL.replace(
                    "        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n",
                    "        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
                    + declaration,
                    1,
                )
                result = self._run({
                    "validate-game-project-operating-system.yml": mutated,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn("canonical ci-gate checkout must be unconditional and unmasked", result.stdout)

    def test_canonical_gate_checkout_must_precede_evaluator(self) -> None:
        checkout = (
            "      - name: Check out repository\n"
            "        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n\n"
        )
        reordered = VALID_CANONICAL.replace(checkout, "").replace(
            "        run: python tools/evaluate_ci_required_gate.py\n",
            "        run: python tools/evaluate_ci_required_gate.py\n\n" + checkout.rstrip() + "\n",
            1,
        )
        result = self._run({
            "validate-game-project-operating-system.yml": reordered,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical ci-gate must checkout the repository first", result.stdout)

    def test_duplicate_top_level_on_fails_closed(self) -> None:
        mutated = VALID_CANONICAL.replace(
            "jobs:\n",
            "on:\n"
            "  pull_request:\n"
            "    paths:\n"
            "      - docs/**\n"
            "jobs:\n",
            1,
        )
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate protected mapping key 'on'", result.stdout)

    def test_duplicate_top_level_jobs_fails_closed(self) -> None:
        mutated = VALID_CANONICAL + """jobs:
  shadow-validation:
    name: shadow-validation
    runs-on: ubuntu-latest
    steps:
      - run: echo shadowed
"""
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate protected mapping key 'jobs'", result.stdout)

    def test_duplicate_pull_request_trigger_fails_closed(self) -> None:
        mutated = VALID_CANONICAL.replace(
            "on:\n  pull_request:\n",
            "on:\n"
            "  pull_request:\n"
            "  pull_request:\n"
            "    paths-ignore:\n"
            "      - docs/**\n",
            1,
        )
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate protected mapping key 'pull_request'", result.stdout)

    def test_dynamic_job_names_fail_closed_repo_wide(self) -> None:
        variants = (
            "${{ 'ci-gate' }}",
            "${{ 'ci-' }}gate",
        )
        for dynamic_name in variants:
            with self.subTest(dynamic_name=dynamic_name):
                focused = """name: Focused
on:
  pull_request:
    paths:
      - docs/**
jobs:
  dynamic-check:
    name: DYNAMIC_NAME
    runs-on: ubuntu-latest
    steps:
      - run: echo dynamic
""".replace("DYNAMIC_NAME", dynamic_name)
                result = self._run({
                    "validate-game-project-operating-system.yml": VALID_CANONICAL,
                    "focused.yml": focused,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn("dynamic workflow job name is unsupported", result.stdout)

    def test_duplicate_ci_gate_names_fail(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL,
            "focused.yml": VALID_CANONICAL.replace("name: Canonical", "name: Focused"),
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exactly one workflow job must be named ci-gate", result.stdout)

    def test_path_filtered_canonical_pull_request_fails(self) -> None:
        filtered = VALID_CANONICAL.replace(
            "  pull_request:\n", "  pull_request:\n    paths:\n      - docs/**\n"
        )
        result = self._run({"validate-game-project-operating-system.yml": filtered})
        self.assertNotEqual(0, result.returncode)
        self.assertIn("pull_request trigger must not declare paths or paths-ignore", result.stdout)

    def test_supported_mapping_spelling_variants_preserve_gate_detection(self) -> None:
        variants = {
            "quoted name key": VALID_CANONICAL.replace(
                "    name: ci-gate\n", '    "name": ci-gate\n'
            ),
            "space before name colon": VALID_CANONICAL.replace(
                "    name: ci-gate\n", "    name : ci-gate\n"
            ),
            "trailing name comment": VALID_CANONICAL.replace(
                "    name: ci-gate\n", "    name: ci-gate # required context\n"
            ),
            "quoted name scalar": VALID_CANONICAL.replace(
                "    name: ci-gate\n", '    name: "ci-gate"\n'
            ),
            "quoted job id": VALID_CANONICAL.replace(
                "  ci-gate:\n", '  "ci-gate":\n'
            ),
            "quoted guarded scalar": VALID_CANONICAL.replace(
                "    if: always()\n", '    if : "always()" # aggregate after skips\n'
            ),
            "quoted evaluator command": VALID_CANONICAL.replace(
                "        run: python tools/evaluate_ci_required_gate.py\n",
                '        run : "python tools/evaluate_ci_required_gate.py" # exact command\n',
            ),
        }
        for label, canonical in variants.items():
            with self.subTest(label=label):
                result = self._run({
                    "validate-game-project-operating-system.yml": canonical,
                })
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_supported_path_key_variants_are_rejected(self) -> None:
        variants = (
            '    "paths":\n      - docs/**\n',
            "    paths :\n      - docs/**\n",
            '    "paths-ignore":\n      - docs/**\n',
            "    paths-ignore :\n      - docs/**\n",
        )
        for declaration in variants:
            with self.subTest(declaration=declaration):
                filtered = VALID_CANONICAL.replace(
                    "  pull_request:\n", f"  pull_request:\n{declaration}"
                )
                result = self._run({
                    "validate-game-project-operating-system.yml": filtered,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn(
                    "pull_request trigger must not declare paths or paths-ignore",
                    result.stdout,
                )

    def test_canonical_gate_job_must_run_always(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "    if: always()\n", "    if: false\n"
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical ci-gate job must use if: always()", result.stdout)

    def test_canonical_gate_job_must_not_mask_failure(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "    if: always()\n",
                "    if: always()\n    continue-on-error: true\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical ci-gate job must not declare continue-on-error", result.stdout)

    def test_canonical_gate_needs_exactly_the_required_jobs(self) -> None:
        variants = {
            "missing": VALID_CANONICAL.replace("      - publication-validation\n", ""),
            "extra": VALID_CANONICAL.replace(
                "      - platform-smoke-windows\n",
                "      - platform-smoke-windows\n      - unrelated-job\n",
            ),
        }
        for label, canonical in variants.items():
            with self.subTest(label=label):
                result = self._run({
                    "validate-game-project-operating-system.yml": canonical,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn("canonical ci-gate dependencies must match exactly", result.stdout)

    def test_canonical_gate_dependency_order_is_not_semantic(self) -> None:
        reordered = VALID_CANONICAL.replace(
            "      - classify-changes\n"
            "      - docs-validation\n"
            "      - core-regression\n"
            "      - ubuntu-contract\n"
            "      - publication-validation\n"
            "      - platform-smoke-windows\n",
            "      - platform-smoke-windows\n"
            "      - publication-validation\n"
            "      - ubuntu-contract\n"
            "      - core-regression\n"
            "      - docs-validation\n"
            "      - classify-changes\n",
        )
        result = self._run({
            "validate-game-project-operating-system.yml": reordered,
        })
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_canonical_gate_evaluate_step_must_not_use_custom_shell(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "        env:\n", "        shell: bash\n        env:\n"
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must not declare a custom shell", result.stdout)

    def test_canonical_gate_evaluate_step_must_not_be_guarded_or_tolerated(self) -> None:
        variants = (
            "        if: false\n",
            "        continue-on-error: true\n",
        )
        for guard in variants:
            with self.subTest(guard=guard):
                mutated = VALID_CANONICAL.replace(
                    "        env:\n", f"{guard}        env:\n"
                )
                result = self._run({
                    "validate-game-project-operating-system.yml": mutated,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn(
                    "canonical ci-gate evaluator step must be unconditional and unmasked",
                    result.stdout,
                )

    def test_canonical_workflow_must_execute_topology_checker(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - run: echo unchecked\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_canonical_checker_step_must_not_be_disabled(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - if: false\n"
                "        run: python tools/check_ci_required_gate_topology.py\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_docs_validation_job_must_not_be_conditional(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "    name: docs-validation\n",
                "    name: docs-validation\n"
                "    if: false\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_docs_validation_job_must_not_allow_space_before_if_colon(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "    name: docs-validation\n",
                "    name: docs-validation\n"
                "    if : false\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_docs_validation_job_must_not_allow_quoted_if_key(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "    name: docs-validation\n",
                "    name: docs-validation\n"
                '    "if": false\n',
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_canonical_checker_step_must_not_mask_failure(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - run: python tools/check_ci_required_gate_topology.py\n"
                "        continue-on-error: true\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_canonical_checker_step_must_not_allow_space_before_continue_colon(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - run: python tools/check_ci_required_gate_topology.py\n"
                "        continue-on-error : true\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_canonical_checker_step_must_not_allow_quoted_continue_key(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - run: python tools/check_ci_required_gate_topology.py\n"
                '        "continue-on-error": true\n',
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "canonical workflow must execute the Required Check topology checker",
            result.stdout,
        )

    def test_advanced_gate_name_scalars_fail_closed(self) -> None:
        variants = {
            "folded": "    name: >-\n      ci-gate\n",
            "alias": "    name: *required-gate\n",
            "anchor": "    name: &required-gate ci-gate\n",
            "tag": "    name: !!str ci-gate\n",
        }
        for label, declaration in variants.items():
            with self.subTest(label=label):
                mutated = VALID_CANONICAL.replace("    name: ci-gate\n", declaration)
                if label == "alias":
                    mutated = (
                        "x-required-gate: &required-gate ci-gate\n" + mutated
                    )
                result = self._run({
                    "validate-game-project-operating-system.yml": mutated,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn("ambiguous YAML in protected", result.stdout)

    def test_escaped_protected_keys_fail_closed(self) -> None:
        variants = {
            "job name": VALID_CANONICAL.replace(
                "    name: ci-gate\n", '    "na\\u006de": ci-gate\n'
            ),
            "trigger filter": VALID_CANONICAL.replace(
                "  pull_request:\n",
                '  pull_request:\n    "paths\\u002dignore":\n      - docs/**\n',
            ),
            "job guard": VALID_CANONICAL.replace(
                "    if: always()\n", '    "i\\u0066": always()\n'
            ),
        }
        for label, canonical in variants.items():
            with self.subTest(label=label):
                result = self._run({
                    "validate-game-project-operating-system.yml": canonical,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn("ambiguous YAML in protected", result.stdout)

    def test_merge_injection_in_gate_job_fails_closed(self) -> None:
        mutated = VALID_CANONICAL.replace(
            "jobs:\n",
            "x-gate-defaults: &gate-defaults\n"
            "  continue-on-error: true\n"
            "jobs:\n",
        ).replace(
            "  ci-gate:\n",
            "  ci-gate:\n    <<: *gate-defaults\n",
        )
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("ambiguous YAML in protected", result.stdout)

    def test_canonical_gate_requires_every_exact_environment_mapping(self) -> None:
        variants = {
            "missing": VALID_CANONICAL.replace(
                "          WINDOWS_RESULT: ${{ needs.platform-smoke-windows.result }}\n",
                "",
            ),
            "extra": VALID_CANONICAL.replace(
                "          WINDOWS_RESULT: ${{ needs.platform-smoke-windows.result }}\n",
                "          WINDOWS_RESULT: ${{ needs.platform-smoke-windows.result }}\n"
                "          UNRELATED_RESULT: success\n",
            ),
        }
        for label, canonical in variants.items():
            with self.subTest(label=label):
                result = self._run({
                    "validate-game-project-operating-system.yml": canonical,
                })
                self.assertNotEqual(0, result.returncode)
                self.assertIn(
                    "canonical ci-gate environment mappings must match exactly",
                    result.stdout,
                )

    def test_canonical_gate_has_only_the_evaluator_step(self) -> None:
        mutated = VALID_CANONICAL.replace(
            "      - name: Evaluate required validation jobs\n",
            "      - run: echo preflight\n"
            "      - name: Evaluate required validation jobs\n",
        )
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exactly two steps", result.stdout)

    def test_canonical_gate_rejects_replaced_evaluator_command(self) -> None:
        mutated = VALID_CANONICAL.replace(
            "python tools/evaluate_ci_required_gate.py\n",
            "python tools/allow_ci_required_gate.py\n",
            1,
        )
        result = self._run({
            "validate-game-project-operating-system.yml": mutated,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exact evaluator command", result.stdout)

    def test_realistic_duplicate_gate_and_path_filter_report_together(self) -> None:
        filtered = VALID_CANONICAL.replace(
            "  pull_request:\n", "  pull_request:\n    paths:\n      - docs/**\n"
        )
        result = self._run({
            "validate-game-project-operating-system.yml": filtered,
            "validate-base-v9-rc.yml": LEGACY_FOCUSED_WORKFLOW,
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exactly one workflow job must be named ci-gate", result.stdout)
        self.assertIn("pull_request trigger must not declare paths or paths-ignore", result.stdout)

    def test_current_repository_topology_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(ROOT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
