/* Shared public-shell presentation. The head boot owns rolling-24h eligibility. */
(() => {
  "use strict";
  const root = document.documentElement;
  const overlay = document.querySelector("[data-brand-intro-overlay]");
  if (!overlay) return;
  const started = Number(root.dataset.brandIntro);
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const mark = overlay.querySelector(".k-brand-intro-mark");
  const wordmark = overlay.querySelector(".k-brand-intro-wordmark");
  const eyes = [...overlay.querySelectorAll('[data-korsac-part="eyes"]')];
  const glow = mark.querySelector("filter")?.id;
  const active = [];
  let timeout;
  let closed = false;
  const cleanup = () => {
    if (closed) return;
    closed = true;
    clearTimeout(timeout);
    reduced.removeEventListener("change", onPreference);
    active.forEach((animation) => {
      try {
        animation.cancel();
      } catch {
        /* CSS safety also expires independently. */
      }
    });
    eyes.forEach((eye) => eye.style.removeProperty("filter"));
    root.removeAttribute("data-brand-intro");
    overlay.remove();
  };
  const onPreference = (event) => {
    if (event.matches) cleanup();
  };
  // Follow the visible overlay's clock, not time spent downloading head resources.
  const style = getComputedStyle(overlay);
  const guard = overlay
    .getAnimations?.()
    .find((animation) => animation.animationName === "k-brand-intro-safety");
  const elapsed = Number(guard?.currentTime) || 0;
  if (
    !started ||
    reduced.matches ||
    elapsed < 0 ||
    elapsed >= 1500 ||
    style.display === "none" ||
    [overlay, mark, wordmark, ...eyes].some(
      (el) => typeof el.animate !== "function",
    )
  ) {
    cleanup();
    return;
  }
  // A lost finished promise cannot leave an invisible pointer blocker.
  timeout = setTimeout(cleanup, Math.max(0, 1700 - elapsed));
  reduced.addEventListener("change", onPreference);
  try {
    const duration = (name) => {
      const value = style.getPropertyValue(name).trim();
      return parseFloat(value) * (value.endsWith("ms") ? 1 : 1000);
    };
    const easing = style.getPropertyValue("--k-ease-standard").trim();
    const play = (el, frames, options) => {
      const animation = el.animate(frames, options);
      active.push(animation);
      animation.currentTime = elapsed;
      return animation;
    };
    play(
      mark,
      [
        { opacity: 0, transform: "translateY(6px)" },
        { opacity: 1, transform: "translateY(0)" },
      ],
      {
        duration: duration("--k-intro-mark-duration"),
        easing,
        fill: "both",
      },
    );
    eyes.forEach((eye) => {
      if (glow) eye.style.filter = `url(#${glow})`;
      const animation = play(
        eye,
        [
          { opacity: 0, offset: 0 },
          { opacity: 0.9, offset: 0.14 },
          { opacity: 1, offset: 0.28 },
          { opacity: 1, offset: 0.57 },
          { opacity: 0.35, offset: 0.75 },
          { opacity: 0, offset: 1 },
        ].map((frame) => ({ ...frame, easing })),
        {
          delay: duration("--k-intro-eye-delay"),
          duration: duration("--k-intro-eye-duration"),
        },
      );
      animation.finished.then(
        () => eye.style.removeProperty("filter"),
        () => {},
      );
    });
    play(wordmark, [{ opacity: 0 }, { opacity: 1 }], {
      delay: duration("--k-intro-wordmark-delay"),
      duration: duration("--k-intro-wordmark-duration"),
      easing,
      fill: "both",
    });
    const exit = play(overlay, [{ opacity: 1 }, { opacity: 0 }], {
      delay: duration("--k-intro-exit-delay"),
      duration: duration("--k-intro-exit-duration"),
      easing,
      fill: "forwards",
    });
    exit.finished.then(cleanup, cleanup);
  } catch {
    cleanup();
  }
})();
