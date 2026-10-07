/* Scoped presentation only. Model content comes from the HTML source cards.
   No catalog API, price calculation, persistence, routing or business rules. */
(() => {
  "use strict";

  document.querySelectorAll("[data-catalog-experience]").forEach((root) => {
    const cards = new Map(
      [...root.querySelectorAll("[data-catalog-model]")].map((card) => [
        card.dataset.catalogModel,
        card,
      ]),
    );
    const preview = root.querySelector("[data-catalog-preview]");
    const previewContent = root.querySelector("[data-catalog-preview-content]");
    if (!cards.size || !preview || !previewContent) return;

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
    const panels = new Map();
    const comparison = root.querySelector("[data-catalog-comparison]");
    const compareTemplate = root.querySelector(
      "[data-catalog-compare-template]",
    );
    const checks = [...root.querySelectorAll("[data-catalog-compare]")];
    const modelDialog = root.querySelector("[data-catalog-model-dialog]");
    let modelOpener;
    let lastCompareControl;
    let animations = [];
    let ghost;

    const title = (card) =>
      card
        .querySelector("[data-catalog-title]")
        .textContent.trim()
        .replace(/\s+/g, " ");

    // Derived views; the source cards remain visible and authoritative.
    cards.forEach((card, code) => {
      const panel = document.createElement("div");
      panel.className = "k-catalog-preview-panel";
      panel.dataset.catalogPanel = code;
      panel.append(
        card.querySelector("[data-catalog-content]").cloneNode(true),
      );
      panel.append(
        card.querySelector("[data-catalog-actions]").cloneNode(true),
      );
      const recommendationTemplate = card.querySelector(
        "[data-catalog-recommendation]",
      );
      if (recommendationTemplate) {
        const recommendation = document.createElement("aside");
        recommendation.className = "k-catalog-recommendation";
        recommendation.setAttribute("aria-label", "Другой сценарий");
        recommendation.append(recommendationTemplate.content.cloneNode(true));
        recommendation
          .querySelectorAll("[data-catalog-pick]")
          .forEach((button) => {
            if (!cards.has(button.dataset.catalogPick)) button.remove();
          });
        panel.append(recommendation);
      }
      previewContent.append(panel);
      panels.set(code, panel);

      // The model title selects the detailed preview; the card keeps one CTA.
      // Wrap only after cloning, so the preview retains a plain heading.
      const heading = card.querySelector("[data-catalog-title]");
      const pick = card.querySelector("button[data-catalog-pick]");
      if (pick) {
        pick.className = "k-catalog-title-button";
        pick.replaceChildren(...heading.childNodes);
        heading.append(pick);
      }
    });

    const stopMotion = () => {
      animations.forEach((animation) => animation.cancel());
      animations = [];
      ghost?.remove();
      ghost = undefined;
    };

    const resolve = (panel, oldMedia) => {
      if (reduced.matches || !panel.animate) return;
      const style = getComputedStyle(root);
      const timing = style.getPropertyValue("--k-motion-brand").trim();
      const duration = parseFloat(timing) * (timing.endsWith("ms") ? 1 : 1000);
      const easing = style.getPropertyValue("--k-ease-precision").trim();
      const options = { duration, easing };
      const media = panel.querySelector("[data-catalog-media]");
      const visual =
        media.querySelector(".k-catalog-silhouette, picture, img") || media;
      // A decorative old silhouette resolves out while the new content is
      // already readable. Focus, semantic state and CTA never wait for motion.
      if (oldMedia) {
        ghost = oldMedia.cloneNode(true);
        ghost.className = "k-catalog-media-ghost";
        ghost.setAttribute("aria-hidden", "true");
        ghost.querySelector("figcaption")?.remove();
        media.append(ghost);
        animations.push(
          ghost.animate(
            [
              { opacity: 0.35, transform: "translateX(0)" },
              { opacity: 0, transform: "translateX(6px)" },
            ],
            { ...options, duration: duration / 2, fill: "forwards" },
          ),
        );
      }
      animations.push(
        visual.animate(
          [
            { transform: "translateX(-8px)", clipPath: "inset(0 80% 0 0)" },
            { transform: "translateX(0)", clipPath: "inset(0)" },
          ],
          options,
        ),
        panel.querySelector(".k-catalog-designation").animate(
          [
            { transform: "translateY(6px)", clipPath: "inset(0 65% 0 0)" },
            { transform: "translateY(0)", clipPath: "inset(0)" },
          ],
          options,
        ),
        panel
          .querySelector(".k-catalog-purpose")
          .animate(
            [{ transform: "translateY(6px)" }, { transform: "translateY(0)" }],
            options,
          ),
      );
      const current = animations;
      Promise.allSettled(current.map((animation) => animation.finished)).then(
        () => {
          if (animations === current) stopMotion();
        },
      );
    };

    const select = (code, animate = true) => {
      if (!cards.has(code)) return;
      const previous = root.dataset.catalogSelection;
      const oldMedia = panels
        .get(previous)
        ?.querySelector("[data-catalog-media]");
      stopMotion();
      root.dataset.catalogSelection = code;
      cards.forEach((card, key) => {
        card.dataset.catalogActive = String(key === code);
        const marker = card.querySelector("[data-catalog-selected]");
        if (marker) marker.hidden = key !== code;
      });
      panels.forEach((panel, key) => {
        panel.hidden = key !== code;
        panel.inert = key !== code;
      });
      root
        .querySelectorAll("[data-catalog-pick][aria-pressed]")
        .forEach((button) => {
          button.setAttribute(
            "aria-pressed",
            String(button.dataset.catalogPick === code),
          );
        });
      const rails = [...root.querySelectorAll("[data-catalog-rail]")];
      const parent = rails.find((rail) => rail.dataset.catalogRail === code)
        ?.dataset.catalogParent;
      rails.forEach((rail) => {
        rail.dataset.catalogActive = String(rail.dataset.catalogRail === code);
        rail.dataset.catalogBranch = String(
          Boolean(parent && rail.dataset.catalogRail === parent),
        );
      });
      root.querySelector("[data-catalog-identifier]").textContent = title(
        cards.get(code),
      );
      if (animate && previous !== code) {
        root.querySelector("[data-catalog-selection-status]").textContent =
          `Выбрано: ${title(cards.get(code))}.`;
        resolve(panels.get(code), oldMedia);
      }
    };

    const selectedChecks = () => checks.filter((check) => check.checked);
    const syncCompare = () => {
      if (!checks.length) return; // Compact homepage variant has no comparison.
      const selected = selectedChecks();
      checks.forEach((check) => {
        check.disabled = selected.length >= 3 && !check.checked;
      });
      root.querySelectorAll("[data-catalog-compare-open]").forEach((button) => {
        button.disabled = selected.length < 2;
      });
      const dock = root.querySelector("[data-catalog-compare-dock]");
      if (dock) {
        dock.hidden = selected.length === 0;
        dock.querySelector("[data-catalog-compare-count]").textContent =
          `${selected.length} / 3`;
      }
      const names = selected.map((check) =>
        title(cards.get(check.dataset.catalogCompare)),
      );
      root.querySelector("[data-catalog-compare-status]").textContent =
        `Выбрано ${selected.length} из 3. ` +
        (selected.length === 3
          ? "Чтобы добавить другую модель, снимите одну отметку. "
          : selected.length < 2
            ? "Отметьте минимум две модели. "
            : "") +
        names.join(" · ");
    };

    const renderCompare = () => {
      const selected = selectedChecks();
      if (!comparison || !compareTemplate || selected.length < 2) return;
      comparison.replaceChildren();
      comparison.style.setProperty("--k-compare-count", selected.length);
      const matrix = compareTemplate.content.cloneNode(true);
      const header = matrix.querySelector("thead tr");
      const rows = [
        ...matrix.querySelectorAll("[data-catalog-compare-property]"),
      ];
      const prefix = comparison.closest("dialog").id;
      rows.forEach((row) => {
        row.querySelector("th").id =
          `${prefix}-${row.dataset.catalogCompareProperty}`;
      });
      selected.forEach((check) => {
        const card = cards.get(check.dataset.catalogCompare);
        const model = document.createElement("th");
        model.scope = "col";
        model.id = `${prefix}-${check.dataset.catalogCompare}`;
        model.textContent = title(card);
        header.append(model);
        rows.forEach((row) => {
          const source = card.querySelector(
            `[data-catalog-property="${row.dataset.catalogCompareProperty}"]`,
          );
          const value = document.createElement("td");
          value.headers = `${row.querySelector("th").id} ${model.id}`;
          const full = document.createElement("span");
          full.className = "k-compare-full";
          full.textContent = source.textContent.trim().replace(/\s+/g, " ");
          const compact = document.createElement("span");
          compact.className = "k-compare-compact";
          compact.textContent =
            source.dataset.catalogCompact || full.textContent;
          value.append(full, compact);
          row.append(value);
        });
      });
      comparison.append(matrix);
    };

    root.addEventListener("click", (event) => {
      const pick = event.target.closest("[data-catalog-pick]");
      if (pick && root.contains(pick)) select(pick.dataset.catalogPick);
      if (event.target.closest("[data-catalog-compare-open]")) renderCompare();
      if (event.target.closest("[data-catalog-compare-clear]")) {
        checks.forEach((check) => {
          check.checked = false;
        });
        syncCompare();
        lastCompareControl?.focus({ preventScroll: true });
      }
      const placeholder = event.target.closest("[data-catalog-placeholder]");
      if (placeholder && modelDialog) {
        event.preventDefault();
        const context = placeholder.closest(
          "[data-catalog-model], [data-catalog-panel]",
        );
        const card = cards.get(
          context?.dataset.catalogModel || context?.dataset.catalogPanel,
        );
        if (!card || modelDialog.open) return;
        root.querySelector("[data-catalog-dialog-title]").textContent =
          title(card);
        modelOpener = placeholder;
        modelDialog.showModal();
        document.body.classList.add("k-dialog-open");
      }
    });
    root.addEventListener("change", (event) => {
      if (event.target.matches("[data-catalog-compare]")) {
        lastCompareControl = event.target;
        syncCompare();
      }
    });
    modelDialog?.addEventListener("close", () => {
      if (modelOpener?.isConnected) modelOpener.focus();
    });
    reduced.addEventListener("change", () => {
      if (reduced.matches) stopMotion();
    });

    // Enhanced controls appear only after the local controller is ready.
    root.dataset.catalogReady = "true";
    root.querySelectorAll("[data-catalog-enhanced]").forEach((element) => {
      element.hidden = false;
    });
    root.querySelectorAll("[data-catalog-fallback]").forEach((link) => {
      link.hidden = true;
    });
    select(
      cards.has(root.dataset.catalogSelection)
        ? root.dataset.catalogSelection
        : cards.keys().next().value,
      false,
    );
    syncCompare();
  });
})();
