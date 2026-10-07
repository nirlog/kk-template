/* Public-shell presentation only: native navigation and a single hero boundary. */
(() => {
  "use strict";
  document.querySelectorAll("[data-site-shell]").forEach((header) => {
    const hero = document.querySelector("[data-home-hero]");
    if (
      header.hasAttribute("data-shell-home") &&
      hero &&
      "IntersectionObserver" in window
    ) {
      const observer = new IntersectionObserver(
        ([entry]) => {
          header.dataset.shellOverHero = String(entry.isIntersecting);
        },
        {
          rootMargin: `-${header.getBoundingClientRect().height + 24}px 0px 0px`,
          threshold: 0,
        },
      );
      observer.observe(hero);
    }
    header.querySelectorAll("[data-shell-enhanced]").forEach((control) => {
      control.hidden = false;
    });
    header.querySelectorAll("[data-shell-fallback]").forEach((fallback) => {
      fallback.hidden = true;
    });
  });
})();
