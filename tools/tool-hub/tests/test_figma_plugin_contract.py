from __future__ import annotations

import json
from pathlib import Path


BASE_ROOT = Path(__file__).resolve().parents[3]
BRIDGE_ROOT = BASE_ROOT / "tools" / "figma-bridge"


def test_manifest_template_is_development_only_and_localhost_bounded() -> None:
    manifest = json.loads((BRIDGE_ROOT / "manifest.template.json").read_text(encoding="utf-8"))

    assert manifest["name"] == "Base Tool Hub Figma Bridge"
    assert manifest["id"] == "FIGMA_ASSIGNED_PLUGIN_ID"
    assert manifest["api"] == "1.0.0"
    assert manifest["editorType"] == ["figma"]
    assert manifest["documentAccess"] == "dynamic-page"
    assert manifest["main"] == "code.js"
    assert manifest["ui"] == "ui.html"
    assert manifest["networkAccess"]["allowedDomains"] == ["none"]
    assert manifest["networkAccess"]["devAllowedDomains"] == ["http://127.0.0.1:8764"]
    assert "*" not in json.dumps(manifest["networkAccess"])


def test_bridge_does_not_request_private_figma_file_key_or_arbitrary_destination_input() -> None:
    code = (BRIDGE_ROOT / "code.js").read_text(encoding="utf-8")
    ui = (BRIDGE_ROOT / "ui.html").read_text(encoding="utf-8")
    combined = code + ui

    assert "figma.fileKey" not in combined
    assert "enablePrivatePluginApi" not in (BRIDGE_ROOT / "manifest.template.json").read_text(encoding="utf-8")
    for forbidden in (
        "figma-file-key-input",
        "node-id-input",
        "project-id-input",
        "project-root-input",
        "destination-url-input",
    ):
        assert forbidden not in combined


def test_bridge_requires_exact_route_marker_before_mutation() -> None:
    code = (BRIDGE_ROOT / "code.js").read_text(encoding="utf-8")

    assert "figma.getNodeByIdAsync(job.generation_area_node_id)" in code
    assert "Base Tool Hub Route · ${job.project_id}" in code
    assert "marker.parent === target" in code
    assert "FIGMA_ROUTE_MARKER_MISSING" in code
    assert "figma.createImage(new Uint8Array(bytes))" in code
    assert "target.appendChild(node)" in code


def test_bridge_ui_hashes_exact_bytes_before_requesting_figma_mutation() -> None:
    ui = (BRIDGE_ROOT / "ui.html").read_text(encoding="utf-8")

    assert "crypto.subtle.digest('SHA-256'" in ui
    assert "X-Content-SHA256" in ui
    assert "CONTENT_HASH_MISMATCH" in ui
    assert "/bridge/jobs/next" in ui
    assert "/content" in ui
    assert "/receipt" in ui
    assert "/release" in ui


def test_bridge_token_is_kept_in_figma_client_storage_not_document_nodes() -> None:
    code = (BRIDGE_ROOT / "code.js").read_text(encoding="utf-8")

    assert "figma.clientStorage.setAsync" in code
    assert "figma.clientStorage.getAsync" in code
    assert "figma.clientStorage.deleteAsync" in code
    assert "setPluginData" not in code
    assert "setSharedPluginData" not in code


def test_bridge_is_idempotent_after_lost_receipt_response() -> None:
    code = (BRIDGE_ROOT / "code.js").read_text(encoding="utf-8")

    assert "child.name === job.node_name" in code
    assert "existing" in code
    assert "FIGMA_DUPLICATE_NODE_CONFLICT" in code
