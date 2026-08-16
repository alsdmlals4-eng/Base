(() => {
  const original = document.querySelector("#figma-delivery-button");
  if (!original) return;

  const button = original.cloneNode(true);
  button.textContent = "확정 및 전달";
  original.replaceWith(button);

  const panel = document.querySelector("#figma-delivery-status");
  const deliverySection = button.closest(".delivery-section");
  const statusButton = document.createElement("button");
  statusButton.type = "button";
  statusButton.textContent = "전달 상태 새로고침";
  statusButton.hidden = true;
  deliverySection?.append(statusButton);

  const download = document.createElement("a");
  download.textContent = "확정 아틀라스 다운로드";
  download.hidden = true;
  download.rel = "noopener noreferrer";
  deliverySection?.append(download);

  function mutationHeadersOnly() {
    return { "X-Studio-CSRF": state.config.csrf_token };
  }

  function renderDelivery(result) {
    const details = [
      result.target_node_name,
      result.bridge_state,
      result.delivery_state,
    ].filter(Boolean);
    if (result.pairing_code) details.push(`페어링 코드 ${result.pairing_code}`);
    panel.textContent = details.join(" · ");
    if (result.delivery_status_url) {
      statusButton.dataset.statusUrl = result.delivery_status_url;
      statusButton.hidden = false;
    }
    if (result.download_url) {
      download.href = result.download_url;
      download.hidden = false;
    }
  }

  button.addEventListener("click", async () => {
    if (!state.runId || !state.exported) return;
    setStatus("확정 및 전달 중…");
    const response = await fetch(`/api/runs/${encodeURIComponent(state.runId)}/confirm-delivery`, {
      method: "POST",
      headers: mutationHeadersOnly(),
    });
    const result = await response.json();
    if (!response.ok) {
      panel.textContent = `전달 차단됨: ${result.detail || "확정된 export와 Tool Hub 연결을 확인하세요."}`;
      setStatus("Figma 전달 차단됨", true);
      return;
    }
    renderDelivery(result);
    setStatus(result.status === "CONFIRMED_AND_VERIFIED" ? "Figma 전달 검증됨" : "Figma 전달 대기 중");
  });

  statusButton.addEventListener("click", async () => {
    const url = statusButton.dataset.statusUrl;
    if (!url) return;
    const response = await fetch(url);
    const result = await response.json();
    if (!response.ok) {
      panel.textContent = `상태 확인 차단됨: ${result.detail || "delivery receipt를 확인하세요."}`;
      setStatus("Figma 상태 확인 차단됨", true);
      return;
    }
    renderDelivery(result);
    setStatus(result.status === "CONFIRMED_AND_VERIFIED" ? "Figma 전달 검증됨" : "Figma 전달 상태 확인됨");
  });

  // The download URL is server-issued only after exact atlas confirmation.
  download.dataset.contract = "confirmed-download";
})();
