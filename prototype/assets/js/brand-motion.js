/* SVG eye geometry only. Hero entrance owns its one-shot trigger; UI Kit may replay. */
(() => {
  "use strict";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  document.querySelectorAll("[data-brand-mark-motion]").forEach((mark) => {
    const svg = mark.querySelector("svg");
    const eyes = [...mark.querySelectorAll('[data-korsac-part="eyes"]')];
    const glow = svg?.querySelector("filter")?.id;
    if (!eyes.length) return;
    const supported = eyes.every((eye) => typeof eye.animate === "function");
    const demo = mark.closest("[data-brand-demo]");
    const replay = demo?.querySelector("[data-brand-replay]");
    const status = demo?.querySelector("[data-brand-status]");
    let active = [];
    let generation = 0;
    let played = false;
    const rest = () => {
      eyes.forEach((eye) => eye.style.removeProperty("filter"));
      mark.dataset.brandState = "off";
      if (status)
        status.textContent = !supported
          ? "Анимация недоступна: глаза выключены."
          : reduced.matches
            ? "Reduced Motion: глаза выключены."
            : "Статическое состояние: глаза выключены.";
    };
    const stop = () => {
      generation += 1;
      active.forEach((animation) => animation.cancel());
      active = [];
      rest();
    };
    const flash = (delay) => {
      stop();
      if (reduced.matches || !supported) return;
      const current = generation;
      const style = getComputedStyle(mark);
      const duration = parseFloat(style.getPropertyValue("--k-motion-reveal"));
      const easing = style.getPropertyValue("--k-ease-standard").trim();
      mark.dataset.brandState = "activating";
      if (status) status.textContent = "Краткая активация глаз.";
      active = eyes.map((eye) => {
        if (glow) eye.style.filter = `url(#${glow})`;
        return eye.animate(
          [
            { opacity: 0, offset: 0 },
            { opacity: 0.85, offset: 0.18 },
            { opacity: 1, offset: 0.35 },
            { opacity: 1, offset: 0.48 },
            { opacity: 0.45, offset: 0.7 },
            { opacity: 0, offset: 1 },
          ].map((frame) => ({ ...frame, easing })),
          { duration, delay },
        );
      });
      Promise.all(active.map((animation) => animation.finished)).then(
        () => {
          if (current !== generation) return;
          active = [];
          rest();
        },
        () => {},
      );
    };
    const hero = mark.closest("[data-home-hero]");
    hero?.addEventListener(
      "korsac:hero-enter",
      () => {
        if (played) return;
        played = true;
        const delay = parseFloat(
          getComputedStyle(mark).getPropertyValue("--k-motion-slow"),
        );
        flash(delay);
      },
      { once: true },
    );
    if (replay) {
      replay.hidden = false;
      replay.disabled = reduced.matches || !supported;
      replay.addEventListener("click", () => flash(0));
    }
    reduced.addEventListener("change", (event) => {
      if (event.matches) stop();
      if (replay) replay.disabled = reduced.matches || !supported;
    });
    rest();
  });
})();
