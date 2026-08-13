"""Deterministic Markdown rendering for daily Source analysis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def _md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_scan_markdown(
    analysis: Mapping[str, object],
    review: Mapping[str, object],
    retained_candidate_ids: Sequence[str],
    *,
    model: str,
    run_id: str,
) -> str:
    retained = set(retained_candidate_ids)
    lines = [
        f"# Daily Source Scan — {analysis.get('run_date')}",
        "",
        "```yaml",
        f"run_id: {_md(run_id)}",
        f"model: {_md(model)}",
        "record_evidence_tier: T6_AI_INFERENCE",
        f"adversarial_result: {_md(review.get('result'))}",
        "project_canon_auto_write: false",
        "protected_semantic_auto_write: false",
        "```",
        "",
        "## Scanned Source families",
        "",
    ]
    for source_id in analysis.get("scanned_sources", []):
        lines.append(f"- `{_md(source_id)}`")
    candidates = analysis.get("candidates", [])
    if isinstance(candidates, list):
        for row in candidates:
            if not isinstance(row, dict) or row.get("candidate_id") not in retained:
                continue
            lines += [
                "",
                f"## [{_md(row['title'])}]({_md(row['original_url'])})",
                "",
                f"- Published/updated: `{_md(row['published_or_updated_at'])}`; checked: `{_md(row['checked_at'])}`",
                f"- Evidence: `{_md(row['evidence_tier'])}` / `{_md(row['evidence_status'])}`",
                f"- Source role: `{_md(row['source_role'])}`",
                f"- Source fact: {_md(row['source_fact'])}",
                f"- Context conditions: {_md('; '.join(row['context_conditions']))}",
                f"- Scope / method: {_md(row['scope'])} / {_md(row['sample_or_method'])}",
                f"- Platform/medium: {_md(row['platform_or_medium'])}",
                f"- Commercial/vendor interest: {_md(row['commercial_or_vendor_interest'])}",
                f"- License/copying boundary: {_md(row['license_or_copying_notes'])}",
                f"- Base overlap / owner: `{_md(row['base_overlap'])}` / `{_md(row['existing_owner'])}`",
                f"- Decision delta: {_md(row['decision_delta'])}",
                f"- Smallest change: {_md(row['smallest_change_candidate'])}",
                f"- Disposition: `{_md(row['disposition'])}` / `{_md(row['work_disposition'])}`",
                f"- Claim ceiling: {_md(row['claim_ceiling'])}",
                f"- Counterevidence: {_md('; '.join(row['counterevidence']))}",
                f"- Validation artifact: {_md(row['validation_artifact'])}",
                f"- Rollback: {_md(row['rollback_or_discard_condition'])}",
            ]
    new_sources = analysis.get("new_source_candidates", [])
    if isinstance(new_sources, list) and new_sources:
        lines += ["", "## New Source candidates — UNVERIFIED_DISCOVERY", ""]
        for row in new_sources:
            if isinstance(row, dict):
                lines.append(
                    f"- [{_md(row['name'])}]({_md(row['url'])}) — "
                    f"`{_md(row['source_role'])}` — {_md(row['reason'])}"
                )
    reason = analysis.get("no_change_reason")
    if isinstance(reason, str) and reason.strip():
        lines += ["", "## No material decision delta", "", _md(reason)]
    findings = review.get("findings", [])
    lines += ["", "## Independent adversarial review", ""]
    if isinstance(findings, list) and findings:
        for row in findings:
            if isinstance(row, dict):
                lines.append(
                    f"- `{_md(row['severity'])}` `{_md(row['decision'])}` "
                    f"[{_md(row['candidate_id'])}] {_md(row['claim'])}"
                )
    else:
        lines.append("- No validated blocking adversarial finding remained.")
    lines += [
        "",
        "## Evidence ceiling",
        "",
        "This immutable record preserves cited Source facts and a T6 model synthesis. "
        "Its merge does not promote an external claim to project Canon, runtime fact, "
        "or protected Base policy.",
        "",
    ]
    return "\n".join(lines)
