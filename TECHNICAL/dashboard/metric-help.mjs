// Short calculation notes work with a mouse, keyboard, or touch screen.
let nextId = 0;
const escape = (text) => String(text).replace(/[&<>"']/g, (character) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);

export function helpButton(label, explanation) {
  const id = `calculation-${++nextId}`;
  return `<span class="metric-help"><button type="button" class="metric-help-button" aria-label="How ${escape(label)} is calculated" aria-describedby="${id}" aria-controls="${id}" aria-expanded="false"><span aria-hidden="true">i</span></button><span id="${id}" class="metric-help-popup" role="tooltip" hidden>${escape(explanation)}</span></span>`;
}

export function enableMetricHelp() {
  let active, popup, pinned = false, closeTimer;
  const buttonFor = (target) => target instanceof Element ? target.closest(".metric-help-button") : null;
  const contains = (target) => target instanceof Node && (active?.contains(target) || popup?.contains(target));

  function close() {
    clearTimeout(closeTimer);
    if (active) active.setAttribute("aria-expanded", "false");
    if (popup) popup.hidden = true;
    active = popup = null;
    pinned = false;
  }

  function position() {
    if (!active?.isConnected) return close();
    const anchor = active.getBoundingClientRect();
    const box = popup.getBoundingClientRect();
    const width = document.documentElement.clientWidth;
    const height = window.innerHeight;
    popup.style.left = `${Math.max(12, Math.min(anchor.left, width - box.width - 12))}px`;
    const below = anchor.bottom + 8;
    popup.style.top = `${Math.max(12, Math.min(below + box.height <= height - 12 ? below : anchor.top - box.height - 8, height - box.height - 12))}px`;
  }

  function show(button) {
    clearTimeout(closeTimer);
    if (active === button) return;
    close();
    active = button;
    popup = document.getElementById(button.getAttribute("aria-describedby"));
    popup.hidden = false;
    active.setAttribute("aria-expanded", "true");
    position();
  }

  function deferClose() {
    clearTimeout(closeTimer);
    closeTimer = setTimeout(() => {
      if (!pinned && document.activeElement !== active) close();
    }, 140);
  }

  document.addEventListener("pointerover", (event) => {
    if (event.pointerType === "touch") return;
    const button = buttonFor(event.target);
    if (button) show(button);
    else if (contains(event.target)) clearTimeout(closeTimer);
  });
  document.addEventListener("pointerout", (event) => {
    if (event.pointerType !== "touch" && contains(event.target) && !contains(event.relatedTarget)) deferClose();
  });
  document.addEventListener("focusin", (event) => {
    const button = buttonFor(event.target);
    if (button) show(button);
    else close();
  });
  document.addEventListener("focusout", (event) => {
    if (buttonFor(event.target) && !contains(event.relatedTarget)) close();
  });
  document.addEventListener("click", (event) => {
    const button = buttonFor(event.target);
    if (button) {
      if (active === button && pinned) close();
      else { show(button); pinned = true; }
    } else if (!contains(event.target)) close();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") close();
  });
  window.addEventListener("resize", () => { if (active) position(); });
  document.addEventListener("scroll", () => { if (active) position(); }, true);
  return close;
}
