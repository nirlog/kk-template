/* DOM-driven presentation only. Native controls are the selection authority.
   No API, pricing, compatibility, cart, persistence or generated benchmark data. */
(() => {
  "use strict";
  const explorerStates = [
    "overview",
    "airflow",
    "graphics",
    "platform",
    "storage",
    "validation",
  ];
  const states = new Set(explorerStates);
  const hardwareKeys = new Set(["case", "memory", "storage", "extra-storage"]);
  const inspection = {
    case: "overview",
    memory: "platform",
    storage: "storage",
    "extra-storage": "storage",
  };
  const buildNames = {
    assembly: "сборка и укладка кабелей",
    setup: "BIOS, профиль памяти и вентиляторы",
    testing: "стабильность и совместная нагрузка",
    final: "порты, сеть и финальный осмотр",
  };

  document
    .querySelectorAll("[data-product-experience]")
    .forEach((experience) => {
      const config = experience.querySelector("[data-prototype-config]");
      const selectedControl = (key) =>
        [
          ...(config?.querySelectorAll(`[data-summary-key="${key}"]`) || []),
        ].find(
          (control) => control instanceof HTMLSelectElement || control.checked,
        );
      const selectedValue = (key) => {
        const control = selectedControl(key);
        return control instanceof HTMLSelectElement
          ? control.selectedOptions[0]
          : control;
      };
      const readSelection = () =>
        Object.fromEntries(
          [...hardwareKeys].map((key) => [
            key,
            selectedValue(key)?.dataset.summaryValue ||
              experience
                .querySelector(`[data-stage-output="${key}"]`)
                ?.textContent.trim() ||
              "—",
          ]),
        );

      const createStage = (stage) => {
        const explorer = stage.closest("[data-product-explorer]");
        const panels = [
          ...(explorer || stage).querySelectorAll("[data-stage-panel]"),
        ];
        const annotations = [
          ...(explorer?.querySelectorAll("[data-explorer-annotation]") || []),
        ];
        const navigation = [
          ...(explorer?.querySelectorAll("[data-explorer-step]") || []),
        ];
        const requestMotion = (kind) => {
          stage.dataset.stageMotion = kind;
          stage.dispatchEvent(
            new CustomEvent("korsac:stage-motion", { bubbles: true }),
          );
        };
        // The stage DOM owns the inspection state; detail/counter/navigation
        // are derived here. CPU/memory are platform subannotations, not slides.
        const setStageState = (state, context = {}) => {
          if (!states.has(state)) return;
          const annotation = context.annotation || state;
          const panelKey = explorer ? state : annotation;
          if (
            panels.length &&
            !panels.some((panel) => panel.dataset.stagePanel === panelKey)
          )
            return;
          const changed =
            stage.dataset.stageState !== state ||
            stage.dataset.stageAnnotation !== annotation ||
            (context.build && stage.dataset.stageBuild !== context.build);
          stage.dataset.stageState = state;
          stage.dataset.stageAnnotation = annotation;
          if (context.build && Object.hasOwn(buildNames, context.build))
            stage.dataset.stageBuild = context.build;
          panels.forEach((panel) => {
            panel.hidden = panel.dataset.stagePanel !== panelKey;
            if (explorer) panel.inert = panel.hidden;
          });
          annotations.forEach((panel) => {
            panel.hidden = panel.dataset.explorerAnnotation !== annotation;
          });
          stage
            .querySelectorAll("[data-stage-choice]")
            .forEach((button) =>
              button.setAttribute(
                "aria-pressed",
                String(button.dataset.stageChoice === state),
              ),
            );
          stage
            .querySelectorAll("[data-stage-hotspot]")
            .forEach((button) =>
              button.setAttribute(
                "aria-expanded",
                String(button.dataset.stageHotspot === annotation),
              ),
            );
          const selection = readSelection();
          const technical = {
            overview: "SYSTEM / OVERVIEW",
            airflow: "SYSTEM / AIRFLOW",
            graphics: "GPU / RTX 5070",
            platform: `PLATFORM / ${selection.memory}`,
            storage: `STORAGE / ${selection.storage}`,
            validation: `BUILD / ${stage.dataset.stageBuild.toUpperCase()}`,
          };
          const marker = stage.querySelector("[data-stage-context]");
          if (marker)
            marker.textContent =
              annotation === "memory"
                ? `MEMORY / ${selection.memory}`
                : technical[state];
          (explorer || stage)
            .querySelectorAll("[data-stage-build-label]")
            .forEach((label) => {
              label.textContent = `Что проверяем: ${buildNames[stage.dataset.stageBuild] || buildNames.assembly}`;
            });
          if (explorer) {
            const index = explorerStates.indexOf(state);
            explorer.querySelector("[data-explorer-counter]").textContent =
              `${String(index).padStart(2, "0")} / ${String(explorerStates.length - 1).padStart(2, "0")}`;
            explorer.querySelector("[data-explorer-identifier]").textContent =
              state.toUpperCase();
            navigation.forEach((button) => {
              const direction = Number(button.dataset.explorerStep);
              const destination = explorerStates[index + direction];
              const label = destination
                ? stage
                    .querySelector(`[data-stage-choice="${destination}"]`)
                    .textContent.trim()
                : direction < 0
                  ? "Назад"
                  : "Далее";
              button.disabled = !destination;
              button.textContent = direction < 0 ? `← ${label}` : `${label} →`;
            });
          }
          if (
            context.animate !== false &&
            (changed || context.force || context.caseChanged)
          )
            requestMotion(context.caseChanged ? "case" : "context");
        };
        stage
          .querySelectorAll("[data-stage-interaction]")
          .forEach((element) => {
            element.hidden = false;
          });
        stage.addEventListener("click", (event) => {
          const button = event.target.closest(
            "[data-stage-choice], [data-stage-hotspot]",
          );
          if (!button || !stage.contains(button)) return;
          const annotation = button.dataset.stageHotspot;
          const state =
            annotation === "cpu" || annotation === "memory"
              ? "platform"
              : annotation || button.dataset.stageChoice;
          setStageState(state, {
            annotation: annotation || state,
          });
        });
        navigation.forEach((button) => {
          button.addEventListener("click", () => {
            if (button.disabled) return;
            const index = explorerStates.indexOf(stage.dataset.stageState);
            setStageState(
              explorerStates[index + Number(button.dataset.explorerStep)],
            );
          });
        });
        stage.dataset.stageBuild ||= "assembly";
        setStageState("overview", { animate: false });
        return { stage, setStageState };
      };
      const controllers = [
        ...experience.querySelectorAll("[data-product-stage]"),
      ].map(createStage);
      const refreshSelection = (key, animate = false) => {
        const selection = readSelection();
        for (const [field, label] of Object.entries(selection)) {
          experience
            .querySelectorAll(`[data-stage-output="${field}"]`)
            .forEach((output) => {
              output.textContent = label;
            });
        }
        const chosenVariant = selectedValue("case")?.dataset.stageCase;
        const variant = ["standard", "north", "minimal"].includes(chosenVariant)
          ? chosenVariant
          : "standard";
        const extra =
          selectedValue("extra-storage")?.dataset.stageDrive === "installed";
        controllers.forEach(({ stage, setStageState }) => {
          const caseChanged = stage.dataset.stageCase !== variant;
          stage.dataset.stageCase = variant;
          stage.dataset.stageExtra = String(extra);
          const role = stage.dataset.stageRole;
          const inspect =
            (role === "configurator" || role === "playground") && key;
          const state = inspect ? inspection[key] : stage.dataset.stageState;
          const annotation = inspect
            ? key === "memory"
              ? "memory"
              : state
            : stage.dataset.stageAnnotation || state;
          setStageState(state, {
            annotation,
            animate,
            caseChanged,
            force: animate && role !== "hero",
          });
        });
      };
      refreshSelection();
      config?.addEventListener("change", (event) => {
        const key = event.target.dataset.summaryKey;
        if (hardwareKeys.has(key)) refreshSelection(key, true);
      });
      config?.addEventListener("focusin", (event) => {
        const key = event.target.dataset.summaryKey;
        if (!hardwareKeys.has(key)) return;
        controllers
          .filter(({ stage }) =>
            ["configurator", "playground"].includes(stage.dataset.stageRole),
          )
          .forEach(({ setStageState }) =>
            setStageState(inspection[key], {
              annotation: key === "memory" ? "memory" : inspection[key],
            }),
          );
      });

      experience.querySelectorAll("[data-enhanced]").forEach((element) => {
        element.hidden = false;
      });
      experience.dataset.experienceReady = "true";

      const measurement = experience.querySelector(
        "[data-measurement-controls]",
      );
      const updateMeasurement = () => {
        const inputs = [
          ...measurement.querySelectorAll("[data-measurement-input]"),
        ];
        const kind = inputs.find(
          (input) => input.dataset.measurementInput === "metric",
        ).value;
        experience
          .querySelectorAll("[data-measurement-kind]")
          .forEach((card) => {
            card.dataset.measurementActive = String(
              card.dataset.measurementKind === kind,
            );
          });
        experience.querySelector("[data-measurement-context]").textContent =
          `${inputs.map((input) => input.selectedOptions[0].textContent.trim()).join(" · ")} · 2560 × 1440. Данные и методика — после тестирования производственной ревизии.`;
      };
      if (measurement) {
        measurement.addEventListener("change", updateMeasurement);
        updateMeasurement();
      }

      const activateBuild = (button) => {
        const step = button.dataset.buildStep;
        if (!Object.hasOwn(buildNames, step)) return;
        experience
          .querySelectorAll("[data-build-step]")
          .forEach((control) =>
            control.setAttribute("aria-pressed", String(control === button)),
          );
        const detail = experience.querySelector("[data-build-detail]");
        if (detail) {
          detail.querySelector("[data-build-label]").textContent =
            step.toUpperCase();
          detail.querySelector("[data-build-title]").textContent = button
            .closest("li")
            .querySelector("h3").textContent;
          detail.querySelector("[data-build-copy]").textContent = button
            .closest("li")
            .querySelector("p")
            .textContent.trim();
        }
        controllers
          .filter(({ stage }) => stage.dataset.stageRole !== "hero")
          .forEach(({ setStageState }) =>
            setStageState("validation", { build: step }),
          );
      };
      experience.querySelectorAll("[data-build-step]").forEach((button) => {
        button.addEventListener("click", () => activateBuild(button));
        button.addEventListener("focus", () => activateBuild(button));
      });
    });
})();
