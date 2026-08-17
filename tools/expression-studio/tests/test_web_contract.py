from pathlib import Path


WEB_ROOT = Path(__file__).parents[1] / "web"


def test_web_exposes_separate_face_gaze_and_head_pose_controls() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")

    assert "얼굴 제어" in html
    assert "시선" in html
    assert "머리 방향" in html
    assert "확정 및 전달" in html


def test_web_confirms_selected_candidate_directly_to_tool_hub_delivery() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="confirm-delivery-button" type="button" disabled' in html
    assert 'id="export-button"' not in html
    assert 'id="delivery-button"' not in html
    assert "/confirm-delivery" in script
    assert "/figma-delivery" not in script
    assert "matching project GPT workspace" not in script
    assert "project_save" in script
    assert "figma_delivery" in script
    assert "target_node_name" in script


def test_web_exposes_optional_download_only_after_confirmation() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="download-copy-button" type="button" disabled' in html
    assert "PC 사본 다운로드" in html
    assert "DOWNLOAD_READY" in script
    assert "download_url" in script
    assert "downloadCopyButton.disabled = true" in script
    assert "downloadCopyButton.disabled = result.download_state !== \"DOWNLOAD_READY\"" in script
    assert "downloadCopyButton.dataset.url = result.download_url" in script


def test_web_guides_figma_pairing_and_refreshes_verified_delivery_without_editable_route() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="figma-open-link"' in html
    assert 'id="pairing-info"' in html
    assert 'id="refresh-delivery-button" type="button" disabled' in html
    assert "Figma 열기" in html
    assert "Figma 상태 새로고침" in html
    assert "function trustedFigmaUrl(" in script
    assert 'parsed.protocol !== "https:"' in script
    assert 'parsed.hostname !== "www.figma.com"' in script
    assert '!parsed.pathname.startsWith("/design/")' in script
    assert "PAIRING_REQUIRED" in script
    assert "pairing_code" in script
    assert "delivery_status_url" in script
    assert "figmaOpenLink.href = trustedFigmaUrl(result.figma_url)" in script
    assert "refreshDeliveryButton.dataset.url = result.delivery_status_url" in script
    assert "await request(refreshDeliveryButton.dataset.url)" in script
    for forbidden in (
        'id="figma-url-input"',
        'id="target-node-input"',
        'id="figma-file-key-input"',
    ):
        assert forbidden not in html


def test_web_renders_resolved_controls_and_anchor_lineage_for_review() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="review-metadata"' in html
    assert "anchor_sha256" in script
    assert "resolved_expression.controls" in script


def test_web_bootstraps_read_only_project_identity_and_blocks_simulated_delivery() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="project-id" readonly' in html
    assert 'value="demo"' not in html
    assert 'request("/api/config")' in script
    assert "delivery_eligible" in script


def test_expression_web_exposes_import_first_controls_without_auto_confirmation() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="candidate-files"' in html
    assert 'name="candidates"' in html
    assert "multiple" in html
    assert 'id="declared-source"' in html
    for source in ("CHATGPT_INCLUDED", "FIGMA_INCLUDED", "LOCAL_GENERATOR", "OTHER_USER_SUPPLIED"):
        assert f'value="{source}"' in html
    assert "추가 비용 없는 가져오기" in html + script
    assert 'id="confirm-delivery-button" type="button" disabled' in html
    assert "출처 선택은 구독·라이선스 증명이 아닙니다" in html
    assert "selectedCandidate = null" in script


def test_expression_web_exposes_canonical_chatgpt_pro_same_run_handoff() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="handoff-controls"' in html
    assert 'id="prepare-handoff-button" type="button"' in html
    assert 'id="handoff-prompt"' in html
    assert 'id="handoff-run-info"' in html
    assert 'id="handoff-anchor-link"' in html
    assert 'id="import-handoff-button" type="button" disabled' in html
    assert "ChatGPT Pro 프롬프트 준비" in html
    assert "승인 원본 다운로드" in html
    assert "같은 Run으로 후보 가져오기" in html
    assert "let pendingHandoffRunId = null" in script
    assert 'request("/api/handoff-runs"' in script
    assert 'request(`/api/handoff-runs/${pendingHandoffRunId}/import`' in script
    assert "pendingHandoffRunId = result.run_id" in script
    assert "handoffPrompt.value = result.prompt" in script
    assert 'handoffAnchorLink.href = result.anchor_url' in script
    assert 'handoffAnchorLink.download = result.source.filename' in script
    assert "body.append(\"candidates\", file)" in script
    assert "renderImportedRun(run, payload)" in script
    assert 'request("/api/import-runs"' in script


def test_expression_web_cost_copy_and_import_requirements_follow_server_run_mode() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="cost-title"' in html
    assert 'id="cost-detail"' in html
    assert 'id="import-controls"' in html
    assert "유료 API를 호출하지 않습니다" not in html
    assert "function applyRunModeUi()" in script
    assert 'studioConfig.run_mode === "subscription_handoff_import"' in script
    assert "OpenAI API 별도 과금 모드" in script
    assert ".required = importMode" in script


def test_expression_web_clears_previous_run_before_every_new_submission() -> None:
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert "function resetRunState()" in script
    submit_start = script.index('document.querySelector("#expression-form").addEventListener("submit"')
    reset_call = script.index("resetRunState();", submit_start)
    request_start = script.index("const payload = requestPayload();", submit_start)

    assert reset_call < request_start
    for marker in (
        "currentRunId = null",
        "currentRunDeliveryEligible = false",
        'document.querySelector("#delivery-result").textContent = ""',
        'downloadCopyButton.dataset.url = ""',
        'figmaOpenLink.removeAttribute("href")',
        'refreshDeliveryButton.dataset.url = ""',
    ):
        assert marker in script


def test_expression_web_blocks_handoff_prepare_until_expression_input_is_valid() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="handoff-readiness"' in html
    assert "function updateHandoffPreparationState()" in script
    assert "prepareHandoffButton.disabled" in script
    assert "controlsFromForm().length > 0" in script
    assert 'document.querySelector("#preset").value' in script
    assert "표정 프리셋 또는 얼굴 제어를 하나 이상 선택하세요." in script


def test_expression_web_formats_structured_validation_errors_instead_of_object_object() -> None:
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert "function responseErrorMessage(payload)" in script
    assert "Array.isArray(detail)" in script
    assert "item.msg" in script
    assert "[object Object]" not in script
    assert "throw new Error(responseErrorMessage(payload))" in script
