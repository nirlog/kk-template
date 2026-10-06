/* Presentation only. All prices, statuses and product data are static mocks.
   No pricing, cart, persistence, search, network or Bitrix integration. */
(() => {
  "use strict";

  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const tabs = [...group.querySelectorAll('[role="tab"]')];
    const select = (selected) => {
      tabs.forEach((tab) => {
        const active = tab === selected;
        tab.setAttribute("aria-selected", String(active));
        tab.tabIndex = active ? 0 : -1;
        document.getElementById(tab.getAttribute("aria-controls")).hidden =
          !active;
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
    panel.hidden = button.getAttribute("aria-expanded") !== "true";
    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(expanded));
      panel.hidden = !expanded;
    });
  });

  document.querySelectorAll("dialog").forEach((dialog) => {
    let opener;
    const triggers = [
      ...document.querySelectorAll("[data-dialog-open]"),
    ].filter((button) => button.dataset.dialogOpen === dialog.id);
    triggers.forEach((button) =>
      button.addEventListener("click", () => {
        opener = button;
        dialog.showModal(); // Native focus containment, Escape and inert background.
        document.body.classList.add("k-dialog-open");
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
      if (!document.querySelector("dialog[open]"))
        document.body.classList.remove("k-dialog-open");
      triggers.forEach((trigger) => {
        if (trigger.hasAttribute("aria-expanded"))
          trigger.setAttribute("aria-expanded", "false");
      });
      if (opener) opener.focus();
    });
    dialog
      .querySelectorAll("a")
      .forEach((link) => link.addEventListener("click", () => dialog.close()));
  });

  const toastRegion = document.querySelector("[data-toast-region]");
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
        button.focus();
      });
      notice.append(message, close);
      toastRegion.replaceChildren(notice);
    });
  });
})();
