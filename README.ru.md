# AgentBox

[English](README.md) · [简体中文](README.zh-CN.md) · [Français](README.fr.md) · [Deutsch](README.de.md)

[![Star History Chart](https://api.star-history.com/svg?repos=sirius1024/agentbox&type=Date)](https://www.star-history.com/#sirius1024/agentbox&Date)

**AgentBox — это открытая продуктовая идея, MVP-спецификация и набор prompt’ов для создания легковесных менеджеров runtime для нескольких AI-агентов.**

Он помогает разработчикам использовать предпочитаемый coding agent, чтобы создавать системы, запускающие множество изолированных, долгоживущих экземпляров AI-агентов на персональном компьютере, домашнем сервере, лабораторной машине или небольшом командном сервере.

Этот репозиторий не является фиксированной реализацией. Это переиспользуемый продуктовый brief и библиотека prompt’ов для Codex, Claude Code, Kimi Code, OpenClaw, Cursor или любого другого coding agent.

---

## Для кого это

AgentBox предназначен для разработчиков, которые хотят:

- запускать несколько выделенных AI-агентов на одной машине;
- дать каждому агенту собственную память, sessions, config, workspace и runtime home;
- не писать вручную container scripts и не копировать API keys;
- использовать coding agent для генерации собственной реализации;
- fork’ать, remix’ить или расширять продуктовую идею.

Если вы ищете готовый устанавливаемый продукт, этот репозиторий пока не является им. Это спецификация и prompt kit для создания такого продукта.

---

## Быстрый старт: передайте AgentBox вашему coding agent

### 1. Выберите стартовую точку

| Ситуация | Prompt |
| --- | --- |
| Начать новую реализацию | `prompts/00-build-from-scratch.md` |
| Добавить core domain и CRUD | `prompts/01-core-crud.md` |
| Добавить Podman/container lifecycle | `prompts/02-podman-runtime.md` |
| Добавить Hermes Agent runtime | `prompts/03-hermes-runtime.md` |
| Добавить backup/restore/diagnose/upgrade | `prompts/04-lifecycle-backup.md` |
| Добавить Web Console | `prompts/05-web-console.md` |
| Нужен короткий общий prompt | `prompts/variants/minimal.md` |

### 2. Дайте coding agent контекст

Передайте ему этот репозиторий или вставьте эти файлы:

```text
README.ru.md или README.md
docs/vision.md
docs/mvp-spec.md
docs/safety-rules.md
prompts/<selected-prompt>.md
```

### 3. Используйте прямую постановку задачи

```text
Use the AgentBox product spec and prompt kit as input.
Implement the milestone in prompts/<selected-prompt>.md.
Keep the implementation simple and focused.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
Add tests and explain how to run them.
```

Вы можете использовать любой branch workflow, stack или coding agent. Правила безопасности и acceptance criteria важнее точной структуры файлов.

---

## Как итерировать при изменении требований

AgentBox рассчитан на развитие через prompt-driven iteration. Когда вы меняете или добавляете требования, не говорите coding agent просто «продолжай». Дайте ему ясный delta.

Рекомендуемый цикл:

1. **Сначала опишите изменение**
   - Обновите свои notes, `docs/mvp-spec.md` или создайте новый prompt в `prompts/`.
   - Держите изменение достаточно маленьким, чтобы его можно было проверить.

2. **Объясните coding agent, что изменилось**
   - Новое поведение;
   - изменённое поведение;
   - удалённое поведение;
   - ограничения, которые должны остаться верными.

3. **Определите acceptance criteria**
   - Какие команды, тесты, UI flows или demos доказывают, что изменение работает?

4. **Попросите обновить docs/prompts, если изменилось продуктовое поведение**
   - Код не должен расходиться с prompt kit.

5. **Проверьте результат по правилам безопасности**
   - Особенно mounts, secrets, isolation и command execution.

### Шаблон prompt для изменения требований

```text
We are iterating on an AgentBox implementation.

Context:
- Read README.md, docs/mvp-spec.md, docs/safety-rules.md, and the relevant prompt under prompts/.
- Preserve the existing product intent: one-machine, isolated, long-running agent instances.

Requirement change:
- Add/change/remove: <describe the exact requirement delta>

Must keep:
- No host-home mount.
- No host-root mount.
- No Docker/Podman socket mount.
- No other-agent data mount.
- No secret leakage.
- No unsafe shell command concatenation.

Out of scope:
- <list what should not be implemented in this iteration>

Acceptance criteria:
- <test/demo/check 1>
- <test/demo/check 2>
- <test/demo/check 3>

Tasks:
1. Update the implementation.
2. Add or update tests.
3. Update docs or prompts if behavior changed.
4. Summarize what changed, how to run it, and what remains out of scope.
```

---

## Ключевая продуктовая идея

AgentBox должен сделать хостинг персональных и small-team агентов таким же простым, как создание управляемых app instances:

1. создать owner;
2. создать agent для этого owner;
3. выбрать runtime, например Hermes Agent, OpenClaw или другой agent framework;
4. запустить agent в изолированном долгоживущем контейнере или sandbox;
5. подключить его через native interface или gateway runtime;
6. мониторить, чинить, делать backup, restore и upgrade.

У каждого agent должны быть собственные:

- runtime home;
- workspace;
- memory и sessions;
- configuration;
- login state;
- lifecycle.

---

## Непереговорные правила безопасности

Любая AgentBox-подобная реализация должна сохранять эти правила:

- без зависимости от Docker Desktop;
- не монтировать host home в agent runtimes;
- не монтировать host root;
- не монтировать данные другого agent;
- не монтировать Docker или Podman sockets;
- не печатать secret values через CLI, API, logs или UI;
- не использовать небезопасную shell string concatenation для runtime commands.

Подробности см. в `docs/safety-rules.md`.

---

## Что должно оставаться неизменным

- одна машина в первую очередь;
- много изолированных, долгоживущих agent instances;
- один owner может иметь несколько agents;
- в MVP один agent принадлежит одному owner;
- поддержка platform-level model provider/key;
- изоляция через container или sandbox;
- рекомендуется Podman/rootless-first runtime.

---

## Что можно менять

Можно свободно remix’ить:

- язык реализации;
- backend framework;
- database;
- UI design;
- coding agent;
- branch workflow;
- prompt style;
- runtime driver;
- deployment model;
- порядок milestones.

Предлагаемый stack, если нужен ориентир:

- Python + FastAPI;
- Typer CLI;
- SQLite;
- React + Vite + TypeScript;
- Podman/rootless Podman.

---

## Структура репозитория

```text
docs/
  vision.md                  # продуктовая идея и постановка проблемы
  mvp-spec.md                # требуемое MVP-поведение
  architecture-principles.md # модель runtime и isolation
  safety-rules.md            # непереговорные ограничения безопасности
  acceptance-demo.md         # demo checklist для полезных реализаций

prompts/
  00-build-from-scratch.md
  01-core-crud.md
  02-podman-runtime.md
  03-hermes-runtime.md
  04-lifecycle-backup.md
  05-web-console.md
  variants/
    minimal.md
    codex.md
    claude-code.md
    kimi-code.md
```

---

## Не-цели MVP

Не позволяйте первой полезной реализации уходить в:

- SaaS multi-tenancy;
- Kubernetes orchestration;
- enterprise RBAC/audit;
- marketplace features;
- serverless/Knative wake-up;
- замену messaging gateway;
- зависимость от Docker Desktop;
- небезопасные host mounts или secret leaks.

Эти темы могут стать будущими экспериментами, но не должны доминировать в MVP.

---

## Текущий статус

Этот репозиторий сейчас является продуктовой идеей, MVP-спецификацией и prompt kit.

Ранее существовавший implementation code был намеренно удалён из main branch, чтобы проект оставался открытым, remix-friendly и удобным для coding agents.

Будущие contributors могут добавлять reference implementations в явно названную директорию, например:

```text
reference-implementations/python-fastapi/
```

---

## License

MIT. See [LICENSE](LICENSE).
