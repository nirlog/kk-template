/* Presentation only. All prices, statuses and product data are static mocks.
   No pricing, cart, persistence, search, network or Bitrix integration. */
(() => {
  "use strict";

  // Motion adds a finite signal to content that is already visible and usable.
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const activeMotion = new Map();
  const motionKinds = new Set([
    "hero",
    "selection",
    "validation",
    "passport",
    "index",
  ]);

  const stopMotion = (target) => {
    const state = activeMotion.get(target);
    if (!state) return;
    state.frames.forEach((frame) => cancelAnimationFrame(frame));
    clearTimeout(state.timeout);
    target.removeEventListener("animationend", state.onEnd);
    target.removeEventListener("animationcancel", state.onEnd);
    target.classList.remove(state.className);
    activeMotion.delete(target);
  };

  const runMotion = (target, className = "k-motion-run") => {
    if (!target) return;
    stopMotion(target);
    target.classList.remove(className);
    if (reducedMotion.matches || !target.isConnected) return;

    const state = { className, frames: [], timeout: undefined, onEnd: null };
    activeMotion.set(target, state);
    const current = () => activeMotion.get(target) === state;
    // Two frames restart the CSS animation without a forced layout. A later
    // replay cancels both frames, so rapid clicks cannot leave stale classes.
    state.frames.push(
      requestAnimationFrame(() => {
        if (!current()) return;
        state.frames.push(
          requestAnimationFrame(() => {
            if (!current()) return;
            if (reducedMotion.matches || !target.isConnected) {
              stopMotion(target);
              return;
            }
            target.classList.add(className);
            const animations = target.getAnimations
              ? target.getAnimations({ subtree: true }).filter((animation) => {
                  const timing = animation.effect?.getComputedTiming();
                  return (
                    "animationName" in animation &&
                    timing &&
                    Number.isFinite(timing.endTime)
                  );
                })
              : [];
            state.onEnd = () => {
              if (
                current() &&
                animations.length > 0 &&
                animations.every(
                  (animation) =>
                    animation.playState === "finished" ||
                    animation.playState === "idle",
                )
              )
                stopMotion(target);
            };
            target.addEventListener("animationend", state.onEnd);
            target.addEventListener("animationcancel", state.onEnd);
            // Account for all staggered children and pseudo-elements. The
            // fallback also cleans up if a section closes before animationend.
            const duration = target.getAnimations
              ? Math.max(
                  0,
                  ...animations.map(
                    (animation) => animation.effect.getComputedTiming().endTime,
                  ),
                )
              : 1600;
            state.timeout = setTimeout(() => {
              if (current()) stopMotion(target);
            }, duration + 80);
          }),
        );
      }),
    );
  };

  // A scoped scene can request the same finite/reduced-motion cleanup without
  // exposing a global stage object or replaying the narrative hero sequence.
  document.addEventListener("korsac:stage-motion", (event) => {
    if (
      event.target instanceof Element &&
      event.target.matches("[data-product-stage]")
    ) {
      runMotion(event.target, "k-stage-resolve");
      const detail = event.target
        .closest("[data-product-explorer]")
        ?.querySelector("[data-explorer-detail]");
      if (detail) runMotion(detail, "k-explorer-resolve");
    }
  });

  // Tabs and disclosure panels retain native content/hidden semantics.
  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const tabs = [...group.querySelectorAll('[role="tab"]')];
    const select = (selected) => {
      tabs.forEach((tab) => {
        const active = tab === selected;
        tab.setAttribute("aria-selected", String(active));
        tab.tabIndex = active ? 0 : -1;
        const panel = document.getElementById(
          tab.getAttribute("aria-controls"),
        );
        if (panel) panel.hidden = !active;
      });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => select(tab));
      tab.addEventListener("keydown", (event) => {
        let target;
        if (event.key === "ArrowRight")
          target = tabs[(index + 1) % tabs.length];
        if (event.key === "ArrowLeft")
          target = tabs[(index - 1 + tabs.length) % tabs.length];
        if (event.key === "Home") target = tabs[0];
        if (event.key === "End") target = tabs[tabs.length - 1];
        if (!target) return;
        event.preventDefault();
        select(target);
        target.focus();
      });
    });
    select(
      tabs.find((tab) => tab.getAttribute("aria-selected") === "true") ||
        tabs[0],
    );
  });

  document.querySelectorAll("[data-accordion]").forEach((button) => {
    const panel = document.getElementById(button.getAttribute("aria-controls"));
    if (!panel) return;
    panel.hidden = button.getAttribute("aria-expanded") !== "true";
    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(expanded));
      panel.hidden = !expanded;
      if (expanded) runMotion(panel, "k-accordion-enter");
      else stopMotion(panel);
    });
  });

  // Native dialogs provide Escape, inert background and focus containment.
  document.querySelectorAll("dialog").forEach((dialog) => {
    let opener;
    const triggers = [
      ...document.querySelectorAll("[data-dialog-open]"),
    ].filter((button) => button.dataset.dialogOpen === dialog.id);
    triggers.forEach((button) =>
      button.addEventListener("click", (event) => {
        // Utility links retain an explanatory destination without JavaScript.
        event.preventDefault();
        if (dialog.open) return;
        opener = button;
        dialog.showModal();
        document.body.classList.add("k-dialog-open");
        runMotion(dialog, "k-dialog-enter");
        triggers.forEach((trigger) => {
          if (trigger.hasAttribute("aria-expanded"))
            trigger.setAttribute("aria-expanded", "true");
        });
      }),
    );
    dialog.querySelectorAll("[data-dialog-close]").forEach((button) => {
      button.addEventListener("click", () => dialog.close());
    });
    dialog.addEventListener("keydown", (event) => {
      if (event.key !== "Tab") return;
      const controls = [
        ...dialog.querySelectorAll(
          'a[href], button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex="0"]',
        ),
      ].filter((control) => control.getClientRects().length > 0);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (!first || !last) return;
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    dialog.addEventListener("click", (event) => {
      const rect = dialog.getBoundingClientRect();
      if (
        event.target === dialog &&
        (event.clientX < rect.left ||
          event.clientX > rect.right ||
          event.clientY < rect.top ||
          event.clientY > rect.bottom)
      )
        dialog.close();
    });
    dialog.addEventListener("close", () => {
      stopMotion(dialog);
      if (!document.querySelector("dialog[open]"))
        document.body.classList.remove("k-dialog-open");
      triggers.forEach((trigger) => {
        if (trigger.hasAttribute("aria-expanded"))
          trigger.setAttribute("aria-expanded", "false");
      });
      if (opener?.isConnected) opener.focus();
    });
    dialog
      .querySelectorAll("a")
      .forEach((link) => link.addEventListener("click", () => dialog.close()));
  });

  const toastRegion = document.querySelector("[data-toast-region]");
  if (toastRegion)
    document.querySelectorAll("[data-toast]").forEach((button) => {
      button.addEventListener("click", () => {
        const notice = document.createElement("div");
        notice.className = "k-notice";
        if (button.dataset.toastKind === "error")
          notice.classList.add("k-notice--error");
        const message = document.createElement("span");
        message.textContent = button.dataset.toast;
        const close = document.createElement("button");
        close.type = "button";
        close.className = "k-button k-button--icon";
        close.setAttribute("aria-label", "Закрыть уведомление");
        close.textContent = "×";
        close.addEventListener("click", () => {
          notice.remove();
          if (button.isConnected) button.focus();
        });
        notice.append(message, close);
        toastRegion.replaceChildren(notice);
      });
    });

  // Presentation labels only: this whitelist intentionally excludes price.
  // Regression guard: hero, summary and product prices remain static HTML;
  // .k-price is never a synchronization target and no price arithmetic exists.
  const summaryKeys = [
    "case",
    "memory",
    "storage",
    "extra-storage",
    "os",
    "software",
    "service",
  ];
  document.querySelectorAll("[data-prototype-config]").forEach((config) => {
    const controls = [...config.querySelectorAll("[data-summary-key]")].filter(
      (control) =>
        control instanceof HTMLSelectElement ||
        (control instanceof HTMLInputElement &&
          ["radio", "checkbox"].includes(control.type)),
    );
    const displayLabel = (control) => {
      const option =
        control instanceof HTMLSelectElement
          ? control.selectedOptions[0]
          : null;
      return (
        option?.dataset.summaryValue ??
        control.dataset.summaryValue ??
        ""
      ).trim();
    };
    const updateLabel = (key, animate) => {
      const group = controls.filter(
        (control) => control.dataset.summaryKey === key,
      );
      if (!group.length) return;
      const empty = key === "service" ? "Базовый сервис" : "Не выбрано";
      const checkboxes = group.filter((control) => control.type === "checkbox");
      const selected = group.find(
        (control) => control instanceof HTMLSelectElement || control.checked,
      );
      const label = checkboxes.length
        ? checkboxes
            .filter((control) => control.checked)
            .map(displayLabel)
            .filter(Boolean)
            .join(" · ") || empty
        : (selected && displayLabel(selected)) || empty;
      config
        .querySelectorAll(`[data-summary-output="${key}"]`)
        .forEach((output) => {
          if (output.textContent === label) return;
          output.textContent = label;
          if (animate) {
            runMotion(output, "k-summary-resolve");
            runMotion(output.closest(".k-manifest-row"), "k-row-confirm");
          }
        });
    };
    summaryKeys.forEach((key) => updateLabel(key, false));
    config.addEventListener("change", (event) => {
      const control = event.target;
      if (
        !controls.includes(control) ||
        !summaryKeys.includes(control.dataset.summaryKey)
      )
        return;
      updateLabel(control.dataset.summaryKey, true);
      const option = control.closest('[data-motion="selection"]');
      if (option) runMotion(option);
    });
  });

  // Replay controls demonstrate visual signals without changing form state.
  document.querySelectorAll("[data-motion-replay]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const target = document.getElementById(button.dataset.motionReplay);
      if (!target || !motionKinds.has(target.dataset.motion)) return;
      // UI Kit only: a reviewer chooses a visual state. No timed request or
      // automatic pending → confirmed transition imitates a real calculation.
      if (target.dataset.motion === "validation") {
        const labels = {
          pending: "Пересчитываем…",
          confirmed: "Конфигурация пересчитана · пример",
          error: "Не удалось пересчитать · пример",
        };
        const kind = button.dataset.motionState;
        if (Object.hasOwn(labels, kind)) {
          stopMotion(target);
          Object.keys(labels).forEach((state) =>
            target.classList.toggle(`k-validation--${state}`, state === kind),
          );
          target.querySelector(".k-validation-label").textContent =
            labels[kind];
        }
      }
      runMotion(target);
    });
  });
  document
    .querySelectorAll('[data-motion="hero"][data-motion-auto]')
    .forEach((hero) => runMotion(hero));

  // Observe only selected identity anchors, never the page's ordinary copy.
  const anchors = [...document.querySelectorAll("[data-motion-observe]")]
    .filter((target) => ["passport", "index"].includes(target.dataset.motion))
    .slice(0, 3);
  const revealed = new Set();
  let observer;
  const observeAnchors = () => {
    if (reducedMotion.matches || !("IntersectionObserver" in window)) return;
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          revealed.add(entry.target);
          observer.unobserve(entry.target);
          runMotion(entry.target);
        });
      },
      { threshold: 0.18, rootMargin: "0px 0px -4% 0px" },
    );
    anchors
      .filter((target) => !revealed.has(target))
      .forEach((target) => observer.observe(target));
  };
  observeAnchors();
  reducedMotion.addEventListener("change", () => {
    observer?.disconnect();
    if (reducedMotion.matches) [...activeMotion.keys()].forEach(stopMotion);
    else observeAnchors();
  });
})();
