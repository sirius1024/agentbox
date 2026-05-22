# AgentBox

[English](README.md) · [简体中文](README.zh-CN.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![Star History Chart](https://api.star-history.com/svg?repos=sirius1024/agentbox&type=Date)](https://www.star-history.com/#sirius1024/agentbox&Date)

**AgentBox est une idée produit ouverte, une spécification MVP et un kit de prompts pour construire des gestionnaires légers de runtimes multi-agents.**

Il aide les builders à utiliser leur coding agent préféré pour créer des systèmes capables d’exécuter plusieurs instances d’agents IA isolées et persistantes sur un ordinateur personnel, un serveur domestique, une machine de laboratoire ou un petit serveur d’équipe.

Ce dépôt n’est pas une implémentation figée. C’est un brief produit réutilisable et une bibliothèque de prompts pour Codex, Claude Code, Kimi Code, OpenClaw, Cursor ou tout autre coding agent.

---

## À qui s’adresse ce dépôt ?

AgentBox s’adresse aux builders qui veulent :

- exécuter plusieurs agents IA dédiés sur une seule machine ;
- donner à chaque agent sa propre mémoire, ses sessions, sa configuration, son workspace et son runtime home ;
- éviter d’écrire manuellement des scripts de conteneurs et de copier des clés API ;
- utiliser un coding agent pour générer leur propre implémentation ;
- forker, remixer ou étendre l’idée produit.

Si vous cherchez un produit installable et terminé, ce dépôt ne l’est pas encore. C’est la spécification et le prompt kit pour en créer un.

---

## Démarrage rapide : donner AgentBox à votre coding agent

### 1. Choisissez votre point de départ

| Situation | Prompt à utiliser |
| --- | --- |
| Démarrer une nouvelle implémentation | `prompts/00-build-from-scratch.md` |
| Ajouter le domaine cœur et le CRUD | `prompts/01-core-crud.md` |
| Ajouter le cycle de vie Podman/conteneur | `prompts/02-podman-runtime.md` |
| Ajouter le runtime Hermes Agent | `prompts/03-hermes-runtime.md` |
| Ajouter backup/restore/diagnose/upgrade | `prompts/04-lifecycle-backup.md` |
| Ajouter une Web Console | `prompts/05-web-console.md` |
| Besoin d’un prompt court et général | `prompts/variants/minimal.md` |

### 2. Fournissez le contexte au coding agent

Donnez-lui ce dépôt, ou collez ces fichiers :

```text
README.fr.md ou README.md
docs/vision.md
docs/mvp-spec.md
docs/safety-rules.md
prompts/<selected-prompt>.md
```

### 3. Donnez une instruction directe

```text
Use the AgentBox product spec and prompt kit as input.
Implement the milestone in prompts/<selected-prompt>.md.
Keep the implementation simple and focused.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
Add tests and explain how to run them.
```

Vous pouvez utiliser n’importe quel workflow de branches, stack technique ou coding agent. Les règles de sécurité et les critères d’acceptation comptent plus que la disposition exacte des fichiers.

---

## Itérer quand les exigences changent

AgentBox est conçu pour évoluer par itérations pilotées par prompts. Quand vous changez ou ajoutez une exigence, ne dites pas seulement à votre coding agent « continue ». Donnez-lui un delta clair.

Boucle recommandée :

1. **Écrivez d’abord le changement**
   - Mettez à jour vos notes, `docs/mvp-spec.md`, ou créez un nouveau prompt sous `prompts/`.
   - Gardez le changement assez petit pour être vérifiable.

2. **Expliquez ce qui a changé**
   - Nouveau comportement ;
   - comportement modifié ;
   - comportement supprimé ;
   - contraintes qui doivent rester vraies.

3. **Définissez les critères d’acceptation**
   - Quelles commandes, tests, flows UI ou démos prouvent que le changement fonctionne ?

4. **Demandez de mettre à jour docs/prompts si le comportement produit change**
   - Le code ne doit pas dériver du prompt kit.

5. **Relisez le résultat avec les règles de sécurité**
   - Surtout les mounts, secrets, isolation et exécution de commandes.

### Modèle de prompt pour changement d’exigence

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

## Idée produit centrale

AgentBox doit rendre l’hébergement d’agents personnels ou de petite équipe aussi simple que la création d’instances applicatives gérées :

1. créer un owner ;
2. créer un agent pour cet owner ;
3. choisir un runtime comme Hermes Agent, OpenClaw ou un autre framework d’agents ;
4. démarrer l’agent dans un conteneur ou sandbox isolé et persistant ;
5. le connecter via l’interface ou gateway native du runtime ;
6. surveiller, réparer, sauvegarder, restaurer et mettre à niveau.

Chaque agent doit avoir son propre :

- runtime home ;
- workspace ;
- mémoire et sessions ;
- configuration ;
- état de connexion ;
- cycle de vie.

---

## Règles de sécurité non négociables

Toute implémentation de type AgentBox doit préserver ces règles :

- aucune dépendance à Docker Desktop ;
- pas de montage du home de l’hôte dans les runtimes d’agents ;
- pas de montage de la racine de l’hôte ;
- pas de montage des données d’un autre agent ;
- pas de montage des sockets Docker ou Podman ;
- aucune valeur secrète imprimée par CLI, API, logs ou UI ;
- pas de concaténation shell non sûre pour construire les commandes runtime.

Voir `docs/safety-rules.md` pour les détails.

---

## Ce qui doit rester cohérent

- priorité à une seule machine ;
- plusieurs agents isolés et persistants ;
- un owner peut avoir plusieurs agents ;
- dans le MVP, un agent appartient à un seul owner ;
- support d’un provider/key de modèle au niveau plateforme ;
- isolation par conteneur ou sandbox ;
- runtime Podman/rootless recommandé.

---

## Ce que vous pouvez changer

Vous êtes encouragé à remixer :

- langage d’implémentation ;
- framework backend ;
- base de données ;
- design UI ;
- coding agent ;
- workflow de branches ;
- style de prompt ;
- runtime driver ;
- modèle de déploiement ;
- ordre des milestones.

Stack suggérée si vous en voulez une :

- Python + FastAPI ;
- Typer CLI ;
- SQLite ;
- React + Vite + TypeScript ;
- Podman/rootless Podman.

---

## Structure du dépôt

```text
docs/
  vision.md                  # idée produit et problème
  mvp-spec.md                # comportement MVP requis
  architecture-principles.md # modèle runtime et isolation
  safety-rules.md            # contraintes de sécurité non négociables
  acceptance-demo.md         # checklist de démonstration utile

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

## Non-objectifs du MVP

Ne laissez pas la première version utile dériver vers :

- multi-tenancy SaaS ;
- orchestration Kubernetes ;
- RBAC/audit d’entreprise ;
- marketplace ;
- wake-up serverless/Knative ;
- remplacement de gateway de messagerie ;
- dépendance à Docker Desktop ;
- montages hôte dangereux ou fuite de secrets.

Ces sujets peuvent devenir des expérimentations futures, mais ne doivent pas dominer le MVP.

---

## Statut actuel

Ce dépôt est actuellement une idée produit, une spécification MVP et un prompt kit.

Le code d’implémentation précédent a été retiré de la branche main pour garder le projet ouvert, remixable et adapté aux coding agents.

Les contributeurs pourront ajouter des implémentations de référence sous un répertoire clairement nommé, par exemple :

```text
reference-implementations/python-fastapi/
```

---

## License

MIT. See [LICENSE](LICENSE).
