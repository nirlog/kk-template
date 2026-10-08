/* Authored cart demo only. Prototype display arithmetic: integer unit amount ×
   quantity, then aggregation. No configuration pricing, network or persistence.
   Production basket/amounts belong to Bitrix Sale / kk.korsac. */
(() => {
  "use strict";
  const money = new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  });
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  document.querySelectorAll("[data-demo-cart]").forEach((root) => {
    const lines = [...root.querySelectorAll("[data-demo-cart-line]")];
    const status = root.querySelector("[data-cart-status]");
    const undo = root.querySelector("[data-cart-undo]");
    const restore = root.querySelector("[data-demo-restore]");
    let removed;
    const activeEffects = new Set();
    const acknowledge = (target) => {
      if (!target?.animate) return;
      const token = reduced.matches
        ? "--k-motion-reduced-base"
        : "--k-motion-base";
      const duration = parseFloat(
        getComputedStyle(root).getPropertyValue(token),
      );
      const animation = target.animate([{ opacity: 0.76 }, { opacity: 1 }], {
        duration,
        easing: "ease-out",
      });
      activeEffects.add(animation);
      animation.finished
        .catch(() => {})
        .finally(() => activeEffects.delete(animation));
    };
    reduced.addEventListener("change", () => {
      activeEffects.forEach((animation) => animation.cancel());
      activeEffects.clear();
    });
    const systemsLabel = (count) => {
      const tail = count % 100;
      const digit = count % 10;
      return `${count} ${tail >= 11 && tail <= 14 ? "систем" : digit === 1 ? "система" : digit >= 2 && digit <= 4 ? "системы" : "систем"}`;
    };
    // Only authored data-demo unit amounts are inputs. Hardware labels are never read.
    const updateDemoCartSummary = (message = "") => {
      let totalMinor = 0;
      let count = 0;
      lines.forEach((line) => {
        const quantity = Number(
          line.querySelector("[data-demo-quantity]").value,
        );
        const unitMinor = Number(line.dataset.demoUnitPriceMinor);
        const lineMinor = unitMinor * quantity;
        line.querySelector("[data-demo-line-total]").textContent = money.format(
          lineMinor / 100,
        );
        line.querySelector('[data-demo-step="-1"]').disabled = quantity <= 1;
        if (!line.hidden) {
          totalMinor += lineMinor;
          count += quantity;
        }
      });
      root
        .querySelectorAll("[data-demo-total], [data-demo-subtotal]")
        .forEach((output) => {
          output.textContent = money.format(totalMinor / 100);
        });
      root.querySelectorAll("[data-demo-system-count]").forEach((output) => {
        output.textContent = systemsLabel(count);
      });
      root.querySelectorAll("[data-demo-config-count]").forEach((output) => {
        const configurations = lines.filter((line) => !line.hidden).length;
        output.textContent = `${configurations} ${configurations === 1 ? "конфигурация" : configurations === 2 ? "конфигурации" : "конфигураций"} PLAY 1440`;
      });
      const filled = root.querySelector("[data-cart-filled]");
      const empty = root.querySelector("[data-cart-empty]");
      if (filled) filled.hidden = count === 0;
      if (empty) empty.hidden = count !== 0;
      if (message && status)
        status.textContent = `${message} ${systemsLabel(count)}. Итого по товарам ${money.format(totalMinor / 100)}. Цены — примеры.`;
    };
    // Fail open to readable authored content if monetary fixtures are malformed.
    if (
      !lines.length ||
      lines.some(
        (line) =>
          !Number.isSafeInteger(Number(line.dataset.demoUnitPriceMinor)) ||
          Number(line.dataset.demoUnitPriceMinor) <= 0,
      )
    )
      return;
    root.querySelectorAll("[data-cart-enhanced]").forEach((control) => {
      control.hidden = false;
    });
    lines.forEach((line) => {
      line.querySelectorAll("[data-demo-step]").forEach((button) => {
        button.addEventListener("click", () => {
          const output = line.querySelector("[data-demo-quantity]");
          const next = Number(output.value) + Number(button.dataset.demoStep);
          const aggregateMinor = lines.reduce(
            (sum, item) =>
              sum +
              (item.hidden
                ? 0
                : Number(item.dataset.demoUnitPriceMinor) *
                  (item === line
                    ? next
                    : Number(
                        item.querySelector("[data-demo-quantity]").value,
                      ))),
            0,
          );
          // Numeric representation guard, not a business quantity limit.
          if (next < 1 || !Number.isSafeInteger(aggregateMinor)) return;
          output.value = String(next);
          updateDemoCartSummary(
            `Количество CONFIG / ${line.dataset.cartConfig} изменено.`,
          );
          if (button.disabled)
            line.querySelector('[data-demo-step="1"]').focus();
          acknowledge(line.querySelector(".k-cart-price"));
        });
      });
      line.querySelector("[data-demo-remove]").addEventListener("click", () => {
        line.hidden = true;
        removed = line;
        if (undo) undo.hidden = false;
        const label = root.querySelector("[data-cart-undo-label]");
        if (label)
          label.textContent = `CONFIG / ${line.dataset.cartConfig} удалена из примера.`;
        updateDemoCartSummary(`CONFIG / ${line.dataset.cartConfig} удалена.`);
        // The removed trigger disappears; keep keyboard position on the undo action.
        restore?.focus();
      });
    });
    restore?.addEventListener("click", () => {
      if (!removed) return;
      removed.hidden = false;
      const target = removed.querySelector("[data-demo-remove]");
      updateDemoCartSummary(
        `CONFIG / ${removed.dataset.cartConfig} восстановлена.`,
      );
      acknowledge(removed);
      if (undo) undo.hidden = true;
      removed = undefined;
      target.focus();
    });
    updateDemoCartSummary();
  });
})();
