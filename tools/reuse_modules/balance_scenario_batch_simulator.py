from __future__ import annotations

import argparse
import copy
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PERCENTILE_METHOD = "LINEAR_INDEX_Q_TIMES_N_MINUS_1"
SWEEP_SUMMARY_STATS = {
    "mean",
    "median",
    "min",
    "max",
    "percentile_05",
    "percentile_25",
    "percentile_75",
    "percentile_95",
}
ADAPTER_EVIDENCE_MODES = {"DIRECT_PROJECT_RULES", "MATHEMATICAL_MODEL"}
ADAPTER_EQUIVALENCE_STATES = {"VERIFIED", "NOT_VERIFIED"}


def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires at least one value")
    if not 0.0 <= q <= 1.0:
        raise ValueError("percentile q must be between 0 and 1")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = q * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return float(
        sorted_values[lower]
        + (sorted_values[upper] - sorted_values[lower]) * fraction
    )


def summarize_values(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"count": 0}
    numeric = sorted(float(value) for value in values)
    count = len(numeric)
    mean = sum(numeric) / count
    if count % 2:
        median = numeric[count // 2]
    else:
        median = (numeric[count // 2 - 1] + numeric[count // 2]) / 2.0
    return {
        "count": count,
        "mean": float(mean),
        "median": float(median),
        "min": float(numeric[0]),
        "max": float(numeric[-1]),
        "percentile_05": _percentile(numeric, 0.05),
        "percentile_25": _percentile(numeric, 0.25),
        "percentile_75": _percentile(numeric, 0.75),
        "percentile_95": _percentile(numeric, 0.95),
    }


def _validate_run(run: dict[str, Any], index: int) -> str:
    seed = run.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError(f"run {index} seed must be an integer")

    variant = run.get("variant")
    if not isinstance(variant, str) or not variant.strip():
        raise ValueError(f"run {index} variant must be a non-empty string")

    metrics = run.get("metrics", {})
    if not isinstance(metrics, dict):
        raise ValueError(f"run {index} metrics must be an object")
    choices = run.get("choices", [])
    if not isinstance(choices, list):
        raise ValueError(f"run {index} choices must be a list")
    failures = run.get("failures", [])
    if not isinstance(failures, list):
        raise ValueError(f"run {index} failures must be a list")

    return variant.strip()


def _variant_report(runs: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, list[float]] = defaultdict(list)
    failure_counts: Counter[str] = Counter()
    choice_counts: Counter[str] = Counter()
    metric_rows: dict[str, list[tuple[float, int]]] = defaultdict(list)

    for run in runs:
        seed = run["seed"]
        for metric_id, value in run.get("metrics", {}).items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"metric {metric_id!r} must be numeric")
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ValueError(f"metric {metric_id!r} must be finite")
            metrics[str(metric_id)].append(numeric)
            metric_rows[str(metric_id)].append((numeric, seed))
        for failure in {str(item) for item in run.get("failures", [])}:
            failure_counts[failure] += 1
        for choice in run.get("choices", []):
            choice_counts[str(choice)] += 1

    run_count = len(runs)
    total_choice_events = sum(choice_counts.values())
    report: dict[str, Any] = {
        "run_count": run_count,
        "metrics": {
            metric_id: summarize_values(values)
            for metric_id, values in sorted(metrics.items())
        },
        "failure_rate_denominator": "RUNS_CONTAINING_TAG",
        "failure_rates": {
            key: (count / run_count if run_count else 0.0)
            for key, count in sorted(failure_counts.items())
        },
        "choice_share_denominator": "TOTAL_CHOICE_EVENTS",
        "choice_event_count": total_choice_events,
        "choice_frequencies": {
            key: {
                "count": count,
                "share": (count / total_choice_events if total_choice_events else 0.0),
            }
            for key, count in sorted(choice_counts.items())
        },
        "dominant_choice": None,
        "tail_runs": {},
    }
    if choice_counts:
        dominant_choice, dominant_count = sorted(
            choice_counts.items(), key=lambda item: (-item[1], item[0])
        )[0]
        report["dominant_choice"] = {
            "choice": dominant_choice,
            "count": dominant_count,
            "share": dominant_count / total_choice_events,
        }

    for metric_id, rows in sorted(metric_rows.items()):
        ordered = sorted(rows, key=lambda row: (row[0], row[1]))
        low = ordered[: min(3, len(ordered))]
        high = ordered[-min(3, len(ordered)) :]
        report["tail_runs"][metric_id] = {
            "lowest": [{"seed": seed, "value": value} for value, seed in low],
            "highest": [
                {"seed": seed, "value": value}
                for value, seed in reversed(high)
            ],
        }
    return report


def _paired_deltas(
    baseline_runs: list[dict[str, Any]],
    candidate_runs: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline_by_seed = {run["seed"]: run for run in baseline_runs}
    candidate_by_seed = {run["seed"]: run for run in candidate_runs}
    shared_seeds = sorted(set(baseline_by_seed) & set(candidate_by_seed))
    metric_deltas: dict[str, list[float]] = defaultdict(list)

    for seed in shared_seeds:
        baseline_metrics = baseline_by_seed[seed].get("metrics", {})
        candidate_metrics = candidate_by_seed[seed].get("metrics", {})
        for metric_id in sorted(set(baseline_metrics) & set(candidate_metrics)):
            baseline_value = baseline_metrics[metric_id]
            candidate_value = candidate_metrics[metric_id]
            if isinstance(baseline_value, bool) or isinstance(candidate_value, bool):
                continue
            if not isinstance(baseline_value, (int, float)) or not isinstance(
                candidate_value, (int, float)
            ):
                continue
            baseline_numeric = float(baseline_value)
            candidate_numeric = float(candidate_value)
            if not math.isfinite(baseline_numeric) or not math.isfinite(candidate_numeric):
                raise ValueError(f"paired metric {metric_id!r} must be finite")
            metric_deltas[str(metric_id)].append(
                candidate_numeric - baseline_numeric
            )

    result: dict[str, Any] = {}
    for metric_id, deltas in sorted(metric_deltas.items()):
        summary = summarize_values(deltas)
        result[metric_id] = {
            "paired_count": len(deltas),
            "mean_delta": summary["mean"],
            "median_delta": summary["median"],
            "min_delta": summary["min"],
            "max_delta": summary["max"],
            "percentile_05_delta": summary["percentile_05"],
            "percentile_95_delta": summary["percentile_95"],
        }
    return result


def _distance_to_target(value: float, low: float, high: float) -> float:
    if low > high:
        low, high = high, low
    if value < low:
        return low - value
    if value > high:
        return value - high
    return 0.0


def _goal_metric_values(
    runs: list[dict[str, Any]], metric_id: str
) -> list[float]:
    values: list[float] = []
    for run in runs:
        metrics = run.get("metrics", {})
        if metric_id not in metrics:
            continue
        value = metrics[metric_id]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError(f"goal metric {metric_id!r} must be finite")
        values.append(numeric)
    return values


def _non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _adapter_evidence_report(manifest: dict[str, Any]) -> dict[str, Any] | None:
    context = manifest.get("analysis_context")
    if context is None:
        return None
    if not isinstance(context, dict):
        raise ValueError("analysis_context must be an object")

    mode = _non_empty_string(
        context.get("adapter_evidence_mode"), "adapter_evidence_mode"
    )
    if mode not in ADAPTER_EVIDENCE_MODES:
        raise ValueError(
            "adapter_evidence_mode must be DIRECT_PROJECT_RULES or MATHEMATICAL_MODEL"
        )

    equivalence = context.get("adapter_equivalence", {})
    if not isinstance(equivalence, dict):
        raise ValueError("adapter_equivalence must be an object")
    status = equivalence.get("status", "NOT_VERIFIED")
    status = _non_empty_string(status, "adapter_equivalence status")
    if status not in ADAPTER_EQUIVALENCE_STATES:
        raise ValueError(
            "adapter_equivalence status must be VERIFIED or NOT_VERIFIED"
        )

    artifact = equivalence.get("validation_artifact")
    if artifact is not None:
        artifact = _non_empty_string(
            artifact, "adapter_equivalence validation_artifact"
        )
    if status == "VERIFIED" and not artifact:
        raise ValueError(
            "adapter_equivalence validation_artifact is required when status is VERIFIED"
        )

    if mode == "MATHEMATICAL_MODEL":
        verified = status == "VERIFIED" and artifact is not None
        if verified:
            ceiling = (
                "MATHEMATICAL_MODEL_EQUIVALENCE_RECORDED_NOT_RUNTIME_OR_PLAYER_PASS"
            )
        else:
            ceiling = (
                "MATHEMATICAL_MODEL_ONLY_RUNTIME_EQUIVALENCE_NOT_VERIFIED"
            )
        required = True
    else:
        verified = False
        ceiling = "DIRECT_RULE_ANALYSIS_NOT_RUNTIME_OR_PLAYER_PASS"
        required = False

    return {
        "mode": mode,
        "equivalence_status": status,
        "validation_artifact": artifact,
        "runtime_equivalence_required": required,
        "runtime_equivalence_verified": verified,
        "claim_ceiling": ceiling,
    }


def _strategy_baseline_reports(
    manifest: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    raw = manifest.get("strategy_baselines", [])
    if not isinstance(raw, list):
        raise ValueError("strategy_baselines must be a list")

    reports: list[dict[str, Any]] = []
    seen_variants: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"strategy baseline {index} must be an object")
        variant = _non_empty_string(
            item.get("variant"), f"strategy baseline {index} variant"
        )
        if variant not in grouped:
            raise ValueError(f"strategy baseline variant {variant!r} not found")
        if variant in seen_variants:
            raise ValueError(f"duplicate strategy baseline variant {variant!r}")
        seen_variants.add(variant)
        strategy_id = _non_empty_string(
            item.get("strategy_id"), f"strategy baseline {index} strategy_id"
        )
        reports.append(
            {
                "variant": variant,
                "strategy_id": strategy_id,
                "role": "BEHAVIORAL_BASELINE",
                "player_skill_truth": False,
                "player_fun_truth": False,
                "difficulty_truth": False,
                "claim_ceiling": "BEHAVIORAL_BASELINE_NOT_PLAYER_EVIDENCE",
            }
        )
    return reports


def _threshold_crossings(
    series: list[dict[str, Any]], target: float
) -> list[dict[str, Any]]:
    crossings: list[dict[str, Any]] = []
    seen: set[float] = set()

    def append_crossing(
        parameter_value: float,
        kind: str,
        between_values: list[float],
    ) -> None:
        key = round(parameter_value, 12)
        if key in seen:
            return
        seen.add(key)
        crossings.append(
            {
                "estimated_parameter_value": float(parameter_value),
                "kind": kind,
                "between_values": between_values,
                "evidence_ceiling": (
                    "OBSERVED_POINT_NOT_PROJECT_TRUTH"
                    if kind == "EXACT_OBSERVED_POINT"
                    else "LINEAR_INTERPOLATION_ESTIMATE_NOT_PROJECT_TRUTH"
                ),
            }
        )

    for index, point in enumerate(series):
        x1 = float(point["parameter_value"])
        y1 = float(point["metric_value"])
        if y1 == target:
            append_crossing(x1, "EXACT_OBSERVED_POINT", [x1, x1])
        if index + 1 >= len(series):
            continue

        next_point = series[index + 1]
        x2 = float(next_point["parameter_value"])
        y2 = float(next_point["metric_value"])
        delta1 = y1 - target
        delta2 = y2 - target
        if delta1 * delta2 < 0.0:
            interpolated = x1 + (target - y1) * (x2 - x1) / (y2 - y1)
            append_crossing(
                interpolated,
                "LINEAR_INTERPOLATION_ESTIMATE",
                [x1, x2],
            )

    return crossings


def _parameter_sweep_reports(
    manifest: dict[str, Any],
    grouped: dict[str, list[dict[str, Any]]],
    variants: dict[str, Any],
) -> list[dict[str, Any]]:
    raw_sweeps = manifest.get("parameter_sweeps", [])
    if not isinstance(raw_sweeps, list):
        raise ValueError("parameter_sweeps must be a list")

    reports: list[dict[str, Any]] = []
    for index, sweep in enumerate(raw_sweeps):
        if not isinstance(sweep, dict):
            raise ValueError(f"parameter sweep {index} must be an object")

        parameter = _non_empty_string(
            sweep.get("parameter"), f"parameter sweep {index} parameter"
        )
        metric = _non_empty_string(
            sweep.get("metric"), f"parameter sweep {index} metric"
        )
        summary_stat = sweep.get("summary_stat", "median")
        summary_stat = _non_empty_string(
            summary_stat, f"parameter sweep {index} summary_stat"
        )
        if summary_stat not in SWEEP_SUMMARY_STATS:
            raise ValueError(
                f"parameter sweep {index} summary_stat must be one of "
                + ", ".join(sorted(SWEEP_SUMMARY_STATS))
            )

        locked_parameters = sweep.get("locked_parameters", [])
        if not isinstance(locked_parameters, list):
            raise ValueError(
                f"parameter sweep {index} locked_parameters must be a list"
            )
        normalized_locks: list[str] = []
        for lock_index, value in enumerate(locked_parameters):
            normalized_locks.append(
                _non_empty_string(
                    value,
                    f"parameter sweep {index} locked parameter {lock_index}",
                )
            )
        if len(normalized_locks) != len(set(normalized_locks)):
            raise ValueError(
                f"parameter sweep {index} locked_parameters must be unique"
            )
        if parameter in normalized_locks:
            raise ValueError("swept parameter cannot also be locked")

        raw_points = sweep.get("points")
        if not isinstance(raw_points, list) or len(raw_points) < 2:
            raise ValueError(
                f"parameter sweep {index} points must contain at least two entries"
            )

        point_values: set[float] = set()
        point_variants: set[str] = set()
        series: list[dict[str, Any]] = []
        seed_sets: list[set[int]] = []

        for point_index, point in enumerate(raw_points):
            if not isinstance(point, dict):
                raise ValueError(
                    f"parameter sweep {index} point {point_index} must be an object"
                )
            raw_value = point.get("value")
            if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
                raise ValueError("sweep point value must be numeric")
            parameter_value = float(raw_value)
            if not math.isfinite(parameter_value):
                raise ValueError("sweep point value must be finite")
            if parameter_value in point_values:
                raise ValueError("sweep point values must be unique")
            point_values.add(parameter_value)

            variant = _non_empty_string(
                point.get("variant"),
                f"parameter sweep {index} point {point_index} variant",
            )
            if variant not in grouped:
                raise ValueError(f"sweep variant {variant!r} not found")
            if variant in point_variants:
                raise ValueError("sweep point variants must be unique")
            point_variants.add(variant)

            metric_summary = variants[variant]["metrics"].get(metric)
            if not metric_summary or metric_summary.get("count", 0) == 0:
                raise ValueError(
                    f"sweep metric {metric!r} not found for variant {variant!r}"
                )
            metric_value = float(metric_summary[summary_stat])
            if not math.isfinite(metric_value):
                raise ValueError(
                    f"sweep metric {metric!r} summary must be finite"
                )

            seed_sets.append({int(run["seed"]) for run in grouped[variant]})
            series.append(
                {
                    "parameter_value": parameter_value,
                    "variant": variant,
                    "metric_value": metric_value,
                }
            )

        first_seed_set = seed_sets[0]
        if any(seed_set != first_seed_set for seed_set in seed_sets[1:]):
            raise ValueError(
                "parameter sweep variants must use the same seed set"
            )

        series.sort(key=lambda item: (item["parameter_value"], item["variant"]))

        target = sweep.get("target")
        crossings: list[dict[str, Any]] = []
        normalized_target: float | None = None
        if target is not None:
            if isinstance(target, bool) or not isinstance(target, (int, float)):
                raise ValueError("parameter sweep target must be numeric")
            normalized_target = float(target)
            if not math.isfinite(normalized_target):
                raise ValueError("parameter sweep target must be finite")
            crossings = _threshold_crossings(series, normalized_target)

        reports.append(
            {
                "parameter": parameter,
                "metric": metric,
                "summary_stat": summary_stat,
                "target": normalized_target,
                "locked_parameters": normalized_locks,
                "locked_parameter_verification": "DECLARED_NOT_RUNTIME_VERIFIED",
                "series": series,
                "seed_set_equal_across_points": True,
                "seed_count_per_point": len(first_seed_set),
                "single_tunable_only": True,
                "automatic_best_value": False,
                "threshold_crossings": crossings,
                "threshold_crossing_count": len(crossings),
                "non_authoritative": True,
            }
        )
    return reports


def analyze_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Analyze project-supplied run records without owning game simulation rules.

    Project adapters remain responsible for producing deterministic records from
    project-authoritative rules. This shared layer only summarizes distributions,
    failure tags, choice-event frequencies, paired-seed deltas, tail runs, bounded
    non-authoritative goal-seek rankings, and declared single-parameter sweep
    evidence. It never mutates project data or treats strategy/model outputs as
    player evidence.
    """

    if manifest.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    project_id = manifest.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError("project_id is required")
    project_id = project_id.strip()

    snapshot = manifest.get("snapshot", {})
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be an object")
    evidence_ceiling = manifest.get("evidence_ceiling", [])
    if not isinstance(evidence_ceiling, list):
        raise ValueError("evidence_ceiling must be a list")

    runs = manifest.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("runs must be a non-empty list")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_variant_seed: set[tuple[str, int]] = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise ValueError(f"run {index} must be an object")
        variant = _validate_run(run, index)
        seed = run["seed"]
        identity = (variant, seed)
        if identity in seen_variant_seed:
            raise ValueError(f"duplicate variant/seed pair: {variant}/{seed}")
        seen_variant_seed.add(identity)
        grouped[variant].append(run)

    variants = {
        variant: _variant_report(grouped[variant]) for variant in sorted(grouped)
    }
    baseline_variant = manifest.get("baseline_variant")
    paired: dict[str, Any] = {}
    if baseline_variant is not None:
        if not isinstance(baseline_variant, str) or not baseline_variant.strip():
            raise ValueError("baseline_variant must be a non-empty string")
        baseline_variant = baseline_variant.strip()
        if baseline_variant not in grouped:
            raise ValueError(f"baseline_variant {baseline_variant!r} not found")
        for candidate in sorted(grouped):
            if candidate == baseline_variant:
                continue
            paired[candidate] = _paired_deltas(
                grouped[baseline_variant], grouped[candidate]
            )

    goal_seek = manifest.get("goal_seek", [])
    if not isinstance(goal_seek, list):
        raise ValueError("goal_seek must be a list")

    goal_seek_reports: list[dict[str, Any]] = []
    for request_index, request in enumerate(goal_seek):
        if not isinstance(request, dict):
            raise ValueError(f"goal_seek request {request_index} must be an object")
        metric_value = request.get("metric")
        if not isinstance(metric_value, str) or not metric_value.strip():
            raise ValueError(f"goal_seek request {request_index} metric is required")
        metric_id = metric_value.strip()
        target = request.get("target")
        if not isinstance(target, list) or len(target) != 2:
            raise ValueError("goal_seek target must be [low, high]")
        if any(
            isinstance(value, bool) or not isinstance(value, (int, float))
            for value in target
        ):
            raise ValueError("goal_seek target values must be numeric")
        low, high = float(target[0]), float(target[1])
        if not math.isfinite(low) or not math.isfinite(high):
            raise ValueError("goal_seek target values must be finite")
        if low > high:
            low, high = high, low

        raw_variants = request.get("variants", sorted(grouped))
        if not isinstance(raw_variants, list):
            raise ValueError("goal_seek variants must be a list")
        requested_variants: list[str] = []
        for value in raw_variants:
            if not isinstance(value, str) or not value.strip():
                raise ValueError("goal_seek variants must contain non-empty strings")
            variant = value.strip()
            if variant not in grouped:
                raise ValueError(f"goal_seek variant {variant!r} not found")
            requested_variants.append(variant)

        ranking = []
        for variant in requested_variants:
            variant_metrics = variants[variant]["metrics"]
            metric_summary = variant_metrics.get(metric_id)
            if not metric_summary or metric_summary.get("count", 0) == 0:
                continue
            median = float(metric_summary["median"])
            distance = _distance_to_target(median, low, high)
            values = _goal_metric_values(grouped[variant], metric_id)
            inside_count = sum(1 for value in values if low <= value <= high)
            inside_share = inside_count / len(values) if values else 0.0
            ranking.append(
                {
                    "variant": variant,
                    "median": median,
                    "distance_to_target": distance,
                    "inside_target": distance == 0.0,
                    "inside_target_count": inside_count,
                    "metric_run_count": len(values),
                    "inside_target_share": inside_share,
                }
            )
        ranking.sort(
            key=lambda item: (
                item["distance_to_target"],
                -item["inside_target_share"],
                item["variant"],
            )
        )
        goal_seek_reports.append(
            {
                "metric": metric_id,
                "target": [low, high],
                "ranking": ranking,
                "non_authoritative": True,
            }
        )

    adapter_evidence = _adapter_evidence_report(manifest)
    strategy_baselines = _strategy_baseline_reports(manifest, grouped)
    parameter_sweeps = _parameter_sweep_reports(manifest, grouped, variants)

    report = {
        "schema_version": 1,
        "project_id": project_id,
        "percentile_method": PERCENTILE_METHOD,
        "snapshot": copy.deepcopy(snapshot),
        "evidence_ceiling": copy.deepcopy(evidence_ceiling),
        "run_count": len(runs),
        "variants": variants,
        "paired_seed_deltas": paired,
        "goal_seek": goal_seek_reports,
        "strategy_baselines": strategy_baselines,
        "parameter_sweeps": parameter_sweeps,
        "mutates_project_data": False,
    }
    if adapter_evidence is not None:
        report["adapter_evidence"] = adapter_evidence
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze deterministic project-supplied balance/scenario run records "
            "without mutating project data"
        )
    )
    parser.add_argument("manifest", type=Path, help="JSON batch-analysis manifest")
    args = parser.parse_args(argv)

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = analyze_manifest(manifest)
    except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print(
            json.dumps(
                {"ok": False, "error": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
