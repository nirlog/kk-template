/* DOM-driven presentation only. Native controls are the selection authority.
   No API, pricing, compatibility, cart, persistence or generated benchmark data. */
(() => {
  "use strict";
  const states = new Set([
    "overview",
    "airflow",
    "graphics",
    "platform",
    "storage",
    "validation",
  ]);
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
        const panels = [...stage.querySelectorAll("[data-stage-panel]")];
        const requestMotion = (kind) => {
          stage.dataset.stageMotion = kind;
          stage.dispatchEvent(
            new CustomEvent("korsac:stage-motion", { bubbles: true }),
          );
        };
        // State belongs to this DOM instance. An annotation is a single panel,
        // not a second copy of hardware selection or a production JSON object.
        const setStageState = (state, context = {}) => {
          if (!states.has(state)) return;
          const annotation = context.annotation || state;
          if (
            panels.length &&
            !panels.some((panel) => panel.dataset.stagePanel === annotation)
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
            panel.hidden = panel.dataset.stagePanel !== annotation;
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
          stage
            .querySelectorAll("[data-stage-build-label]")
            .forEach((label) => {
              label.textContent = `Что проверяем: ${buildNames[stage.dataset.stageBuild] || buildNames.assembly}`;
            });
          if (
            context.animate !== false &&
            (changed || context.force || context.caseChanged)
          )
            requestMotion(context.caseChanged ? "case" : "context");
          if (context.source === "manual")
            stage.dispatchEvent(
              new CustomEvent("korsac:stage-control", {
                bubbles: true,
                detail: { state },
              }),
            );
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
            source: "manual",
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
            .querySelectorAll(
              `[data-stage-output="${field}"], [data-passport-output="${field}"]`,
            )
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
          const state =
            (role === "configurator" || role === "playground") && key
              ? inspection[key]
              : stage.dataset.stageState;
          const annotation =
            key === "memory" &&
            (role === "configurator" || role === "playground")
              ? "memory"
              : state;
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
              source: "config",
            }),
          );
      });

      experience.querySelectorAll("[data-enhanced]").forEach((element) => {
        element.hidden = false;
      });
      experience.dataset.experienceReady = "true";
      experience
        .querySelectorAll("[data-product-explorer]")
        .forEach((explorer) => {
          const controller = controllers.find(({ stage }) =>
            explorer.contains(stage),
          );
          const steps = [
            ...explorer.querySelectorAll("[data-narrative-state]"),
          ];
          if (!controller) return;
          const desktop = window.matchMedia(
            "(min-width: 1100px) and (min-height: 820px)",
          );
          let observer,
            lastCandidate = null,
            manualScrollY = null,
            resizeFrame;
          const markActive = (state) =>
            steps.forEach((step) => {
              const active = step.dataset.narrativeState === state;
              step.dataset.active = String(active);
              if (active) step.setAttribute("aria-current", "step");
              else step.removeAttribute("aria-current");
            });
          const currentStep = () => {
            const line = innerHeight * 0.4;
            const visible = steps
              .map((step) => ({ step, rect: step.getBoundingClientRect() }))
              .filter(({ rect }) => rect.bottom > 0 && rect.top < innerHeight);
            return (
              visible.find(
                ({ rect }) => rect.top <= line && rect.bottom >= line,
              )?.step || null
            );
          };
          const manual = (state) => {
            manualScrollY = window.scrollY;
            lastCandidate = currentStep();
            markActive(state);
          };
          controller.stage.addEventListener("korsac:stage-control", (event) =>
            manual(event.detail.state),
          );
          explorer
            .querySelectorAll("[data-narrative-choice]")
            .forEach((button) =>
              button.addEventListener("click", () => {
                const state = button.dataset.narrativeChoice;
                controller.setStageState(state, { source: "manual" });
              }),
            );
          const observe = () => {
            observer?.disconnect();
            if (!desktop.matches || !("IntersectionObserver" in window)) return;
            observer = new IntersectionObserver(
              () => {
                const candidate = currentStep();
                if (!candidate || candidate === lastCandidate) return;
                // A queued observer callback cannot undo a click at the same scroll
                // position. Only a genuinely new step after scrolling can take over.
                if (
                  manualScrollY !== null &&
                  Math.abs(window.scrollY - manualScrollY) < 8
                )
                  return;
                lastCandidate = candidate;
                manualScrollY = null;
                const state = candidate.dataset.narrativeState;
                controller.setStageState(state, { source: "scroll" });
                markActive(state);
              },
              {
                rootMargin: `-${Math.round(innerHeight * 0.39)}px 0px -${Math.round(innerHeight * 0.59)}px 0px`,
                threshold: 0,
              },
            );
            steps.forEach((step) => observer.observe(step));
          };
          observe();
          desktop.addEventListener("change", observe);
          window.addEventListener("resize", () => {
            cancelAnimationFrame(resizeFrame);
            resizeFrame = requestAnimationFrame(observe);
          });
        });

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
            setStageState("validation", { build: step, source: "build" }),
          );
      };
      experience.querySelectorAll("[data-build-step]").forEach((button) => {
        button.addEventListener("click", () => activateBuild(button));
        button.addEventListener("focus", () => activateBuild(button));
      });
    });
})();
