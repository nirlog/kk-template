/* Internal review specimen only. Never create identity, dates, records or state.
   Real eligibility/transactions belong to shared backend application services. */
(() => {
  "use strict";
  const root = document.querySelector("[data-internal-workflow]");
  if (!root) return;
  root.querySelectorAll("[data-workflow-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const output = button.parentElement.querySelector(
        "[data-action-feedback]",
      );
      output.textContent = `Макет вызова ${button.dataset.workflowAction}. Операция не выполнена; записи и состояние не изменились.`;
    });
  });
  root.querySelectorAll("[data-workflow-form]").forEach((form) => {
    const choices = [...form.querySelectorAll("[data-replacement-choice]")];
    const sync = () =>
      choices.forEach((choice) => {
        const fields = form.querySelector(
          `#${choice.dataset.replacementChoice}`,
        );
        fields.hidden = !choice.checked;
        fields.disabled = !choice.checked;
      });
    choices.forEach((choice) => choice.addEventListener("change", sync));
    sync();
    const check = () => {
      const output = form.querySelector("[data-workflow-feedback]");
      if (choices.length && !choices.some((choice) => choice.checked)) {
        output.textContent =
          "Выберите хотя бы одну фактическую запись компонента.";
        output.dataset.invalid = "";
        choices[0].focus();
        return;
      }
      const invalid = [...form.elements].find(
        (control) => control.willValidate && !control.checkValidity(),
      );
      if (invalid) {
        output.textContent =
          "Заполните обязательные поля выбранной операции. Ничего не сохранено.";
        output.dataset.invalid = "";
        invalid.setAttribute("aria-invalid", "true");
        invalid.reportValidity();
        return;
      }
      delete output.dataset.invalid;
      output.textContent =
        "Форма проверена только в макете. Сервисное событие, компоненты, аудит и гарантия не изменены.";
    };
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      check();
    });
    form
      .querySelector("[data-workflow-check]")
      .addEventListener("click", check);
    form.addEventListener("input", (event) =>
      event.target.removeAttribute("aria-invalid"),
    );
  });
})();
