# AgentBox

[English](README.md) · [简体中文](README.zh-CN.md) · [Français](README.fr.md) · [Русский](README.ru.md)

[![Star History Chart](https://api.star-history.com/svg?repos=sirius1024/agentbox&type=Date)](https://www.star-history.com/#sirius1024/agentbox&Date)

**AgentBox ist eine offene Produktidee, eine MVP-Spezifikation und ein Prompt-Kit zum Bau leichtgewichtiger Multi-Agent-Runtime-Manager.**

Es hilft Buildern, mit ihrem bevorzugten Coding Agent Systeme zu erstellen, die viele isolierte, dauerhaft laufende KI-Agent-Instanzen auf einem persönlichen Computer, Heimserver, Laborrechner oder kleinen Teamserver betreiben.

Dieses Repository ist keine feste Implementierung. Es ist ein wiederverwendbares Produkt-Briefing und eine Prompt-Bibliothek für Codex, Claude Code, Kimi Code, OpenClaw, Cursor oder jeden anderen Coding Agent.

---

## Für wen ist das gedacht?

AgentBox ist für Builder, die:

- mehrere dedizierte KI-Agenten auf einer Maschine betreiben wollen;
- jedem Agenten eigenen Speicher, Sessions, Konfiguration, Workspace und Runtime Home geben wollen;
- keine Container-Skripte manuell schreiben und keine API Keys herumkopieren wollen;
- einen Coding Agent verwenden wollen, um ihre eigene Implementierung zu erzeugen;
- die Produktidee forken, remixen oder erweitern wollen.

Wenn Sie ein fertig installierbares Produkt suchen, ist dieses Repository noch nicht das. Es ist die Spezifikation und das Prompt-Kit, um eines zu erstellen.

---

## Schnellstart: AgentBox an Ihren Coding Agent übergeben

### 1. Wählen Sie Ihren Startpunkt

| Situation | Prompt |
| --- | --- |
| Neue Implementierung starten | `prompts/00-build-from-scratch.md` |
| Core Domain und CRUD hinzufügen | `prompts/01-core-crud.md` |
| Podman-/Container-Lifecycle hinzufügen | `prompts/02-podman-runtime.md` |
| Hermes Agent Runtime hinzufügen | `prompts/03-hermes-runtime.md` |
| Backup/Restore/Diagnose/Upgrade hinzufügen | `prompts/04-lifecycle-backup.md` |
| Web Console hinzufügen | `prompts/05-web-console.md` |
| Kurzen allgemeinen Prompt nutzen | `prompts/variants/minimal.md` |

### 2. Geben Sie dem Coding Agent Kontext

Übergeben Sie ihm dieses Repository oder fügen Sie diese Dateien ein:

```text
README.de.md oder README.md
docs/vision.md
docs/mvp-spec.md
docs/safety-rules.md
prompts/<selected-prompt>.md
```

### 3. Verwenden Sie eine direkte Aufgabenbeschreibung

```text
Use the AgentBox product spec and prompt kit as input.
Implement the milestone in prompts/<selected-prompt>.md.
Keep the implementation simple and focused.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
Add tests and explain how to run them.
```

Sie können jedes Branch-Workflow, jeden Stack oder jeden Coding Agent verwenden. Sicherheitsregeln und Akzeptanzkriterien sind wichtiger als das exakte Dateilayout.

---

## Iteration bei geänderten Anforderungen

AgentBox soll sich durch prompt-gesteuerte Iteration weiterentwickeln. Wenn Sie Anforderungen ändern oder hinzufügen, sagen Sie Ihrem Coding Agent nicht nur „weiter“. Geben Sie ihm ein klares Delta.

Empfohlener Ablauf:

1. **Schreiben Sie die Änderung zuerst auf**
   - Aktualisieren Sie Ihre Notizen, `docs/mvp-spec.md`, oder erstellen Sie einen neuen Prompt unter `prompts/`.
   - Halten Sie die Änderung klein genug, um sie verifizieren zu können.

2. **Sagen Sie dem Coding Agent, was sich geändert hat**
   - Neues Verhalten;
   - geändertes Verhalten;
   - entferntes Verhalten;
   - Constraints, die weiterhin gelten müssen.

3. **Definieren Sie Akzeptanzkriterien**
   - Welche Commands, Tests, UI-Flows oder Demos beweisen, dass die Änderung funktioniert?

4. **Lassen Sie Docs/Prompts aktualisieren, wenn sich Produktverhalten ändert**
   - Code darf nicht vom Prompt-Kit wegdriften.

5. **Prüfen Sie das Ergebnis gegen die Sicherheitsregeln**
   - Besonders Mounts, Secrets, Isolation und Command Execution.

### Prompt-Vorlage für Anforderungsänderungen

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

## Zentrale Produktidee

AgentBox soll persönliches und kleines Team-Agent-Hosting so einfach machen wie das Erstellen verwalteter App-Instanzen:

1. einen Owner erstellen;
2. einen Agenten für diesen Owner erstellen;
3. eine Runtime wie Hermes Agent, OpenClaw oder ein anderes Agent-Framework auswählen;
4. den Agenten in einem isolierten, dauerhaft laufenden Container oder Sandbox starten;
5. ihn über die native Schnittstelle oder Gateway der Runtime verbinden;
6. überwachen, reparieren, sichern, wiederherstellen und aktualisieren.

Jeder Agent sollte eigene Ressourcen haben:

- Runtime Home;
- Workspace;
- Memory und Sessions;
- Konfiguration;
- Login-Zustand;
- Lifecycle.

---

## Nicht verhandelbare Sicherheitsregeln

Jede AgentBox-ähnliche Implementierung sollte diese Regeln einhalten:

- keine Docker-Desktop-Abhängigkeit;
- kein Mounten des Host-Home in Agent-Runtimes;
- kein Mounten des Host-Root;
- kein Mounten von Daten anderer Agenten;
- kein Mounten von Docker- oder Podman-Sockets;
- keine Secret-Werte über CLI, API, Logs oder UI ausgeben;
- keine unsichere Shell-String-Verkettung für Runtime-Commands.

Details siehe `docs/safety-rules.md`.

---

## Was konsistent bleiben sollte

- eine Maschine zuerst;
- viele isolierte, dauerhaft laufende Agent-Instanzen;
- ein Owner kann mehrere Agenten haben;
- im MVP gehört ein Agent genau einem Owner;
- Plattform-Level Model Provider/Key Support;
- Container- oder Sandbox-basierte Isolation;
- Podman/rootless-first Runtime wird empfohlen.

---

## Was Sie ändern können

Sie können frei remixen:

- Implementierungssprache;
- Backend-Framework;
- Datenbank;
- UI-Design;
- Coding Agent;
- Branch-Workflow;
- Prompt-Stil;
- Runtime Driver;
- Deployment-Modell;
- Reihenfolge der Milestones.

Vorgeschlagener Stack, falls Sie einen möchten:

- Python + FastAPI;
- Typer CLI;
- SQLite;
- React + Vite + TypeScript;
- Podman/rootless Podman.

---

## Repository-Struktur

```text
docs/
  vision.md                  # Produktidee und Problemrahmen
  mvp-spec.md                # erforderliches MVP-Verhalten
  architecture-principles.md # Runtime- und Isolationsmodell
  safety-rules.md            # nicht verhandelbare Sicherheitsregeln
  acceptance-demo.md         # Demo-Checkliste für nützliche Implementierungen

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

## MVP-Nichtziele

Lassen Sie die erste nützliche Implementierung nicht abdriften in:

- SaaS-Multi-Tenancy;
- Kubernetes-Orchestrierung;
- Enterprise-RBAC/Audit;
- Marketplace-Features;
- Serverless/Knative Wake-up;
- Ersatz für Messaging-Gateways;
- Docker-Desktop-Abhängigkeit;
- unsichere Host-Mounts oder Secret-Leaks.

Diese Themen können zukünftige Experimente sein, sollten aber das MVP nicht dominieren.

---

## Aktueller Status

Dieses Repository ist derzeit eine Produktidee, MVP-Spezifikation und ein Prompt-Kit.

Früherer Implementierungscode wurde bewusst aus dem main-Branch entfernt, damit das Projekt offen, remixbar und agent-freundlich bleibt.

Zukünftige Beiträge können Referenzimplementierungen in einem klar benannten Verzeichnis hinzufügen, zum Beispiel:

```text
reference-implementations/python-fastapi/
```

---

## License

MIT. See [LICENSE](LICENSE).
