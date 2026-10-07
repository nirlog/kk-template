/* Public-shell presentation: sticky headers and a small homepage top tolerance. */
(() => {
  "use strict";
  const headers = [...document.querySelectorAll("[data-site-shell]")];
  const homeHeaders = headers.filter((header) =>
    header.hasAttribute("data-shell-home"),
  );
  if (homeHeaders.length) {
    let frame;
    const syncTop = () => {
      // Native hash/restoration can occur after deferred scripts. Stay opaque
      // for a pending fragment; load/pageshow/scroll reconcile the actual Y.
      const pendingHash = location.hash && document.readyState !== "complete";
      const atTop = String(window.scrollY <= 16 && !pendingHash);
      homeHeaders.forEach((header) => {
        if (header.dataset.shellAtTop !== atTop)
          header.dataset.shellAtTop = atTop;
      });
    };
    const scheduleTop = () => {
      if (frame !== undefined) return;
      frame = requestAnimationFrame(() => {
        frame = undefined;
        syncTop();
      });
    };
    syncTop();
    window.addEventListener("scroll", scheduleTop, { passive: true });
    window.addEventListener("load", syncTop, { once: true });
    window.addEventListener("pageshow", syncTop);
    window.addEventListener("hashchange", syncTop);
  }
  headers.forEach((header) => {
    header.querySelectorAll("[data-shell-enhanced]").forEach((control) => {
      control.hidden = false;
    });
    header.querySelectorAll("[data-shell-fallback]").forEach((fallback) => {
      fallback.hidden = true;
    });
  });
})();
