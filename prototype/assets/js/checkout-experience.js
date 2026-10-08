/* One-page checkout presentation only. Authored order never persists or sends
   contacts. Property visibility/required flags below are authored demo fixtures,
   not production availability rules. Bitrix owns methods, restrictions and
   order-property sets. Native validity; success is a static document. */
(() => {
  "use strict";
  const root = document.querySelector("[data-checkout-experience]");
  if (!root) return;
  const form = root.querySelector("[data-demo-checkout-form]");
  const buyerRadios = [...form.querySelectorAll('input[name="demo-buyer"]')];
  const company = form.querySelector("[data-company-fields]");
  const companyControls = [...company.querySelectorAll("input")];
  const summary = form.querySelector("[data-checkout-errors]");
  const errorList = summary.querySelector("[data-checkout-error-list]");
  const point = root.querySelector("#demo-point");
  const picker = root.querySelector("[data-delivery-picker]");
  const dialog = document.getElementById("delivery-dialog");
  const deliveryButton = root.querySelector("#delivery-open");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const effects = new Set();
  let attempted = false;
  const acknowledge = (target) => {
    if (!target?.animate) return;
    const duration = parseFloat(
      getComputedStyle(root).getPropertyValue(
        reduced.matches ? "--k-motion-reduced-base" : "--k-motion-base",
      ),
    );
    const animation = target.animate([{ opacity: 0.76 }, { opacity: 1 }], {
      duration,
      easing: "ease-out",
    });
    effects.add(animation);
    animation.finished.catch(() => {}).finally(() => effects.delete(animation));
  };
  reduced.addEventListener("change", () => {
    effects.forEach((effect) => effect.cancel());
    effects.clear();
  });
  const clearError = (control) => {
    control.removeAttribute("aria-invalid");
    const error = document.getElementById(`${control.id}-error`);
    if (error) {
      error.hidden = true;
      error.textContent = "";
    }
  };
  const renderDemoBuyerProperties = () => {
    const isCompany =
      buyerRadios.find((control) => control.checked)?.value === "company";
    company.hidden = !isCompany;
    companyControls.forEach((control) => {
      control.disabled = !isCompany;
      control.required =
        isCompany && control.hasAttribute("data-demo-company-required");
      const label = form.querySelector(`label[for="${control.id}"]`);
      const base = control.dataset.errorLabel;
      label.textContent = `${base}${control.required ? " *" : " · необязательно"}`;
      clearError(control);
    });
    const name = form.querySelector("#buyer-name");
    const nameLabel = isCompany ? "Контактное лицо" : "Имя";
    form.querySelector('label[for="buyer-name"]').firstChild.textContent =
      `${nameLabel} `;
    name.dataset.errorLabel = nameLabel;
  };
  const fieldMessage = (control) => {
    if (control.id === "demo-point")
      return "Выберите демонстрационный пункт выдачи.";
    if (control.id === "order-consent")
      return "Подтвердите согласие с документами макета.";
    if (control.name === "demo-payment") return "Выберите способ оплаты.";
    if (control.validity.typeMismatch && control.type === "email")
      return "Укажите email в формате name@example.ru.";
    return `Заполните поле «${control.dataset.errorLabel || control.id}».`;
  };
  const invalidControls = () => {
    const seen = new Set();
    return [...form.elements].filter((control) => {
      if (!control.willValidate || control.validity.valid) return false;
      const key = control.type === "radio" ? control.name : control.id;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  };
  const renderErrors = (focus = false) => {
    [...form.elements].forEach((control) => {
      if (control.id) clearError(control);
    });
    const errors = invalidControls();
    // Keep existing error links connected during change/blur. Replacing the
    // list on pointer-down focus transfer would swallow the pending click.
    const existing = new Map(
      [...errorList.children].map((item) => [item.dataset.errorKey, item]),
    );
    const remaining = new Set(errors.map((control) => control.id));
    errors.forEach((control) => {
      const message = fieldMessage(control);
      control.setAttribute("aria-invalid", "true");
      const fieldError = document.getElementById(
        control.id === "demo-point"
          ? "demo-point-error"
          : control.name === "demo-payment"
            ? "payment-error"
            : `${control.id}-error`,
      );
      if (fieldError) {
        fieldError.textContent = message;
        fieldError.hidden = false;
      }
      const item = existing.get(control.id) || document.createElement("li");
      item.dataset.errorKey = control.id;
      const link = item.querySelector("a") || document.createElement("a");
      link.href = `#${control.id === "demo-point" ? "delivery-open" : control.id}`;
      link.dataset.errorFor = control.id;
      link.textContent = message;
      if (!link.isConnected) item.append(link);
      if (!item.isConnected) errorList.append(item);
    });
    existing.forEach((item, key) => {
      if (!remaining.has(key)) item.remove();
    });
    const paymentError = root.querySelector("[data-payment-error]");
    if (!errors.some((control) => control.name === "demo-payment"))
      paymentError.hidden = true;
    summary.hidden = errors.length === 0;
    if (focus && errors.length) summary.focus();
    return errors.length === 0;
  };
  // Conditional behavior enhances native fields. Contact controls deliberately
  // have no names: even a no-JS GET navigation cannot serialize personal data.
  form.noValidate = true;
  root.querySelectorAll("[data-checkout-enhanced]").forEach((control) => {
    control.hidden = false;
  });
  root.querySelector("[data-company-fallback]").hidden = true;
  dialog.querySelector("[data-delivery-dialog-content]").append(picker);
  root.querySelector("[data-delivery-fallback]").hidden = true;
  const review = root.querySelector("[data-order-review]");
  const compact = matchMedia("(max-width: 899px)");
  review.open = !compact.matches;
  compact.addEventListener("change", () => {
    review.open = !compact.matches;
  });
  renderDemoBuyerProperties();
  buyerRadios.forEach((control) =>
    control.addEventListener("change", () => {
      renderDemoBuyerProperties();
      acknowledge(
        company.hidden ? form.querySelector(".k-contact-fields") : company,
      );
      if (attempted) renderErrors();
    }),
  );
  form.addEventListener("change", (event) => {
    // Validate choices after activation. Text errors refresh on submit so that
    // blur cannot collapse error rows underneath a pending pointer/touch click.
    if (!event.target.matches('input[type="radio"], input[type="checkbox"]'))
      return;
    if (event.target.matches('input[name="demo-payment"]'))
      acknowledge(event.target.closest(".k-commerce-choice"));
    if (attempted) renderErrors();
  });
  errorList.addEventListener("click", (event) => {
    const link = event.target.closest("[data-error-for]");
    if (!link) return;
    event.preventDefault();
    const control = document.getElementById(link.dataset.errorFor);
    if (control === point) {
      deliveryButton.click();
      point.focus();
    } else control?.focus();
  });
  dialog.querySelector("[data-confirm-point]").addEventListener("click", () => {
    if (!point.checked) {
      point.focus();
      return;
    }
    root.querySelector("[data-delivery-summary]").textContent =
      "Пункт выдачи выбран · пример, без физического адреса.";
    dialog.close();
    clearError(point);
    acknowledge(root.querySelector(".k-delivery-selection"));
    if (attempted) renderErrors();
  });
  // A chosen native radio is valid even if the dialog is dismissed with Escape.
  point.addEventListener("change", () => {
    root.querySelector("[data-delivery-summary]").textContent = point.checked
      ? "Пункт выдачи выбран · пример, без физического адреса."
      : "Пункт выдачи ещё не выбран.";
    if (attempted) renderErrors();
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    attempted = true;
    if (!renderErrors(true)) return;
    // Static navigation only; never submit form payload or store buyer/cart data.
    location.assign("order-success.html");
  });
})();
