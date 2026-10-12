/* Review presentation only. No authentication, verification, ownership or persistence. */
(() => {
  "use strict";
  document.querySelectorAll("[data-account-mount]").forEach((mount) => {
    const content = document.getElementById(mount.dataset.accountMount);
    if (!content) return;
    const fallback = content.closest("[data-account-fallback]");
    mount.append(content);
    fallback.hidden = true;
  });
  document.querySelectorAll("[data-account-form]").forEach((form) => {
    const output = form.querySelector("[data-account-feedback]");
    const validate = () => {
      const confirmation = form.querySelector(
        'input[id$="confirm"],#profile-confirm-password',
      );
      const password = form.querySelector(
        "#register-password,#profile-new-password",
      );
      if (confirmation && password)
        confirmation.setCustomValidity(
          confirmation.value === password.value
            ? ""
            : "Пароли должны совпадать.",
        );
      const invalid = [...form.elements].find(
        (control) => control.willValidate && !control.checkValidity(),
      );
      if (invalid) {
        output.textContent =
          form.dataset.accountForm === "add-system"
            ? "Проверьте формат ID и кода системы. Проверка принадлежности не выполнялась."
            : "Заполните обязательные поля в правильном формате. Ничего не отправлено.";
        output.dataset.invalid = "";
        invalid.setAttribute("aria-invalid", "true");
        invalid.focus();
        invalid.reportValidity();
        return;
      }
      delete output.dataset.invalid;
      const feedback = {
        recovery:
          "Если аккаунт с таким email существует, инструкции будут отправлены. В макете аккаунт не проверяется и письмо не отправляется.",
        "add-system":
          "Форма проверена только в макете. Данные не отправлены, заявка и привязка не созданы. В магазине заявку рассматривает менеджер.",
        profile:
          "Форма проверена только в макете. Контакты и email аккаунта не изменены.",
        password:
          "Форма проверена только в макете. Текущий пароль не проверен, новый пароль не сохранён.",
        register:
          "Форма проверена только в макете. Аккаунт не создан, данные не отправлены.",
        login:
          "Форма проверена только в макете. Вход не выполнен, сессия не создана.",
      };
      output.textContent = feedback[form.dataset.accountForm];
      form
        .querySelectorAll('input[type="password"],[data-system-code-input]')
        .forEach((input) => (input.value = ""));
    };
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      validate();
    });
    form
      .querySelector("[data-account-check]")
      .addEventListener("click", validate);
    form.addEventListener("input", (event) => {
      event.target.removeAttribute("aria-invalid");
      event.target.setCustomValidity("");
    });
  });
  document
    .querySelector("[data-account-unlink]")
    ?.addEventListener("click", () => {
      document.querySelector("[data-unlink-feedback]").textContent =
        "Подтверждение показано только в макете. Связь с аккаунтом, паспорт, гарантия и история не изменены.";
    });
  document
    .querySelector("[data-account-logout]")
    ?.addEventListener("click", () => {
      document.querySelector("[data-account-logout-feedback]").textContent =
        "Макет выхода: сессия не создавалась и не изменялась.";
    });
  document
    .querySelector("#account-add-dialog")
    ?.addEventListener("close", () => {
      document.querySelector("[data-system-code-input]").value = "";
    });
})();
