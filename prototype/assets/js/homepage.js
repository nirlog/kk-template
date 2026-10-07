/* Finite hero presentation. The existing catalog controller owns discovery. */
(() => {
  "use strict";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const active = new Set();
  const stop = () => {
    active.forEach((animation) => animation.cancel());
    active.clear();
  };
  document.querySelectorAll("[data-home-hero]").forEach((hero) => {
    if (!hero.animate) return;
    const style = getComputedStyle(hero);
    const duration = (token) => {
      const raw = style.getPropertyValue(token).trim();
      return parseFloat(raw) * (raw.endsWith("ms") ? 1 : 1000);
    };
    const enter = style.getPropertyValue("--k-ease-enter").trim();
    const precision = style.getPropertyValue("--k-ease-precision").trim();
    const brand = duration("--k-motion-brand");
    const slow = duration("--k-motion-slow");
    const base = duration("--k-motion-base");
    const play = (selector, frames, options) => {
      const target = hero.querySelector(selector);
      if (!target) return;
      const animation = target.animate(frames, options);
      active.add(animation);
      animation.finished.then(
        () => active.delete(animation),
        () => active.delete(animation),
      );
    };
    if (reduced.matches) {
      // Readable from the first frame; no spatial entrance or stagger.
      [
        "[data-home-headline]",
        ".k-home-hero-description",
        ".k-home-hero-actions",
        "[data-home-media]",
      ].forEach((selector) =>
        play(selector, [{ opacity: 0.75 }, { opacity: 1 }], {
          duration: duration("--k-motion-reduced-base"),
          easing: style.getPropertyValue("--k-ease-standard").trim(),
        }),
      );
      return;
    }
    play(".k-home-media-field", [{ opacity: 0.3 }, { opacity: 1 }], {
      duration: slow,
      easing: enter,
    });
    play(
      ".k-home-media-guide",
      [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }],
      { duration: slow, easing: precision },
    );
    play(
      "[data-home-media]",
      [
        { transform: "translateY(16px) scale(.985)" },
        { transform: "translateY(0) scale(1)" },
      ],
      { duration: slow, delay: base / 2, easing: enter },
    );
    play(
      "[data-home-headline]",
      [
        { transform: "translateY(16px)", clipPath: "inset(0 20% 0 0)" },
        { transform: "translateY(0)", clipPath: "inset(0)" },
      ],
      { duration: brand, delay: base, easing: precision },
    );
    play(
      ".k-home-hero-description",
      [{ transform: "translateY(8px)" }, { transform: "translateY(0)" }],
      { duration: brand, delay: brand, easing: enter },
    );
    play(
      ".k-home-hero-actions",
      [{ transform: "translateY(8px)" }, { transform: "translateY(0)" }],
      { duration: base, delay: slow, easing: enter },
    );
    play(
      ".k-home-copper-detail",
      [{ transform: "scaleX(0)" }, { transform: "scaleX(1)" }],
      {
        duration: brand,
        delay: duration("--k-motion-reveal"),
        easing: precision,
      },
    );
  });
  reduced.addEventListener("change", () => {
    // Both preference changes settle entry effects; neither replays them.
    stop();
  });
})();
