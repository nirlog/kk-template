/* Review-only input feedback. No identity resolution, submission or storage. */
(() => {
  "use strict";
  document.querySelectorAll("[data-passport-inquiry]").forEach((form) => {
    const feedback = form.querySelector("[data-inquiry-feedback]");
    const check = () => {
      const invalid = [...form.elements].find(
        (control) => control.willValidate && !control.checkValidity(),
      );
      if (invalid) {
        feedback.textContent =
          "Выберите тему и заполните сообщение. Это проверка макета без отправки.";
        feedback.dataset.invalid = "";
        invalid.setAttribute("aria-invalid", "true");
        invalid.reportValidity();
        return;
      }
      delete feedback.dataset.invalid;
      feedback.textContent =
        "Форма заполнена. Обращение не отправлено: отправка и хранение появятся при интеграции.";
    };
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      check();
    });
    form.querySelector("[data-inquiry-check]").addEventListener("click", check);
    form.addEventListener("input", (event) =>
      event.target.removeAttribute("aria-invalid"),
    );
  });
})();
