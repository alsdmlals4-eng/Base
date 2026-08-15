const BRIDGE_VERSION = "1";
const TOKEN_KEY = "base-tool-hub-figma-bridge-token-v1";
const PENDING_RECEIPT_KEY = "base-tool-hub-figma-bridge-pending-receipt-v1";

figma.showUI(__html__, { width: 380, height: 520, themeColors: true });

function postToUi(message) {
  figma.ui.postMessage(message);
}

function imageFillOf(node) {
  if (!("fills" in node) || !Array.isArray(node.fills)) return null;
  return node.fills.find((fill) => fill && fill.type === "IMAGE" && fill.imageHash) || null;
}

async function sendStoredState() {
  const token = await figma.clientStorage.getAsync(TOKEN_KEY);
  const pendingReceipt = await figma.clientStorage.getAsync(PENDING_RECEIPT_KEY);
  postToUi({
    type: "stored-state",
    token: typeof token === "string" ? token : null,
    pendingReceipt: pendingReceipt || null,
    bridgeVersion: BRIDGE_VERSION,
  });
}

async function applyImage(message) {
  if (figma.editorType !== "figma") {
    throw new Error("FIGMA_EDITOR_REQUIRED");
  }
  const job = message.job;
  const bytes = message.bytes;
  if (!job || !Array.isArray(bytes)) {
    throw new Error("DELIVERY_PAYLOAD_INVALID");
  }
  for (const field of ["target_node_id", "route_parent_node_id", "project_marker_node_id"]) {
    if (!/^\d+[:-]\d+$/.test(job[field] || "")) {
      throw new Error("FIGMA_TARGET_INVALID");
    }
  }
  if (!job.target_node_name || !job.project_marker_name || !job.tool_route_id) {
    throw new Error("FIGMA_ROUTE_IDENTITY_REQUIRED");
  }
  if (!Number.isFinite(job.width) || !Number.isFinite(job.height) || job.width < 1 || job.height < 1) {
    throw new Error("DELIVERY_DIMENSIONS_INVALID");
  }

  const [parent, target, marker] = await Promise.all([
    figma.getNodeByIdAsync(job.route_parent_node_id),
    figma.getNodeByIdAsync(job.target_node_id),
    figma.getNodeByIdAsync(job.project_marker_node_id),
  ]);
  if (!parent || !("children" in parent)) {
    throw new Error("FIGMA_ROUTE_PARENT_UNAVAILABLE");
  }
  if (!target || !("children" in target) || !("appendChild" in target)) {
    throw new Error("FIGMA_TARGET_UNAVAILABLE");
  }
  if (target.parent !== parent || target.name !== job.target_node_name) {
    throw new Error("FIGMA_TARGET_IDENTITY_MISMATCH");
  }
  if (
    !marker ||
    marker.parent !== parent ||
    marker.name !== job.project_marker_name ||
    marker.visible !== false ||
    marker.locked !== true
  ) {
    throw new Error("FIGMA_ROUTE_MARKER_MISSING");
  }

  const existing = target.children.find((child) => child.name === job.node_name);
  let node;
  let imageHash;
  if (existing) {
    const existingFill = imageFillOf(existing);
    if (!existingFill) {
      throw new Error("FIGMA_DUPLICATE_NODE_CONFLICT");
    }
    node = existing;
    imageHash = existingFill.imageHash;
  } else {
    const image = figma.createImage(new Uint8Array(bytes));
    node = figma.createRectangle();
    node.name = job.node_name;
    node.resize(job.width, job.height);
    node.fills = [{ type: "IMAGE", scaleMode: "FIT", imageHash: image.hash }];
    target.appendChild(node);
    imageHash = image.hash;
  }

  const receipt = {
    delivery_id: job.delivery_id,
    created_node_id: node.id,
    created_node_name: node.name,
    target_node_id: target.id,
    content_sha256: job.content_sha256,
    bridge_version: BRIDGE_VERSION,
    image_hash: imageHash,
  };
  await figma.clientStorage.setAsync(PENDING_RECEIPT_KEY, receipt);
  postToUi({ type: "mutation-complete", receipt });
}

figma.ui.onmessage = async (message) => {
  try {
    if (!message || typeof message.type !== "string") {
      throw new Error("BRIDGE_MESSAGE_INVALID");
    }
    if (message.type === "load-state") {
      await sendStoredState();
      return;
    }
    if (message.type === "store-token") {
      if (typeof message.token !== "string" || !message.token) {
        throw new Error("BRIDGE_TOKEN_INVALID");
      }
      await figma.clientStorage.setAsync(TOKEN_KEY, message.token);
      postToUi({ type: "token-stored" });
      return;
    }
    if (message.type === "clear-token") {
      await figma.clientStorage.deleteAsync(TOKEN_KEY);
      await figma.clientStorage.deleteAsync(PENDING_RECEIPT_KEY);
      postToUi({ type: "token-cleared" });
      return;
    }
    if (message.type === "clear-pending-receipt") {
      await figma.clientStorage.deleteAsync(PENDING_RECEIPT_KEY);
      postToUi({ type: "pending-receipt-cleared" });
      return;
    }
    if (message.type === "apply-image") {
      await applyImage(message);
      return;
    }
    throw new Error("BRIDGE_MESSAGE_UNSUPPORTED");
  } catch (error) {
    const detail = error instanceof Error ? error.message : "BRIDGE_OPERATION_FAILED";
    postToUi({ type: "bridge-error", detail });
  }
};

void sendStoredState();
