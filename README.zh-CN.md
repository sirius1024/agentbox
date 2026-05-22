# AgentBox

[English](README.md)

**AgentBox 是一个开放的产品创意、MVP 规格和 Prompt Kit，用于构建轻量级多 Agent 运行时管理器。**

它的目标很简单：让用户可以在一台个人电脑、家用服务器、实验机器或小团队服务器上，轻松运行多个彼此隔离、长期运行的 AI Agent 实例。

AgentBox 不只是一个软件实现。它更像是一个可复用的产品概念：你可以用自己喜欢的 Coding Agent、技术栈、分支流程和设计方式来实现它。

你可以用这个仓库来：

- 理解 AgentBox 的产品想法；
- 复用 MVP 需求和安全规则；
- 把 prompts 交给 Codex、Claude Code、Kimi Code、OpenClaw 或其他 Coding Agent；
- fork、改造、二创，或构建你自己的实现；
- 贡献更好的规格、prompt、图示或参考实现。

---

## 如何把 AgentBox 交给你的 Coding Agent 使用

AgentBox 被设计成一个 **Prompt Kit**。你不需要遵循固定的分支计划，也不需要使用某一个特定的 Coding Agent。

### 方式 A：从零构建一个新实现

1. 创建一个新的空仓库或本地项目。
2. 打开你喜欢的 Coding Agent，例如 Codex、Claude Code、Kimi Code、OpenClaw、Cursor 或其他工具。
3. 把这个仓库作为上下文提供给它，或者把以下文件粘贴给它：
   - `README.zh-CN.md` 或 `README.md`
   - `docs/vision.md`
   - `docs/mvp-spec.md`
   - `docs/safety-rules.md`
   - `prompts/00-build-from-scratch.md`
4. 告诉 Coding Agent：

```text
Use the AgentBox product spec and prompt kit as input.
Build the first useful implementation from prompts/00-build-from-scratch.md.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
```

你也可以用中文描述：

```text
请基于 AgentBox 的产品规格和 Prompt Kit，按照 prompts/00-build-from-scratch.md 构建第一版可用实现。
必须遵守 docs/safety-rules.md 中的安全规则。
先不要实现无关的未来特性。
```

### 方式 B：继续已有实现

如果你已经有一个 AgentBox 类似项目，可以选择与你下一步目标匹配的 milestone prompt：

| 目标 | Prompt |
| --- | --- |
| 从零开始 | `prompts/00-build-from-scratch.md` |
| 增加核心领域模型和 CRUD | `prompts/01-core-crud.md` |
| 增加 Podman / 容器生命周期 | `prompts/02-podman-runtime.md` |
| 增加 Hermes Agent 运行时 | `prompts/03-hermes-runtime.md` |
| 增加备份、恢复、诊断、升级 | `prompts/04-lifecycle-backup.md` |
| 增加 Web Console | `prompts/05-web-console.md` |

可以直接这样给 Coding Agent 布置任务：

```text
Read the AgentBox README, MVP spec, safety rules, and the selected milestone prompt.
Implement only that milestone.
Keep the implementation simple.
Do not violate the safety rules.
Add tests and explain how to run them.
```

中文也可以写成：

```text
请阅读 AgentBox 的 README、MVP 规格、安全规则，以及我选定的 milestone prompt。
只实现这个 milestone，不要顺手做未来功能。
实现保持简单，不能违反安全规则。
请补充测试，并说明如何运行。
```

### 方式 C：使用短 Prompt 版本

如果你的 Coding Agent 已经拥有足够的仓库上下文，可以直接使用这些短 prompt：

- `prompts/variants/minimal.md`
- `prompts/variants/codex.md`
- `prompts/variants/claude-code.md`
- `prompts/variants/kimi-code.md`

所有 prompt 都可以自由修改、缩短、扩展或二创。

### 不应该让 Coding Agent 一开始做什么

第一版实现不要跑偏到：

- SaaS 多租户；
- Kubernetes 编排；
- 企业级 RBAC / 审计；
- Marketplace；
- 自定义消息网关；
- Docker Desktop 依赖；
- 不安全的宿主机挂载或密钥泄漏。

第一版有用实现应该聚焦：**单机、多隔离 Agent、长期运行、可管理、可恢复。**

---

## 为什么需要 AgentBox？

个人和团队 AI Agent 正变得越来越有用，但认真运行多个 Agent 仍然太手工。

一个用户可能希望为不同用途运行独立 Agent：

- 个人助理；
- 编程 Agent；
- 研究 Agent；
- 运维 Agent；
- 家庭使用；
- 小团队支持；
- 对 Hermes Agent、OpenClaw、Claude Code wrapper、Codex CLI wrapper 或其他本地/远程 Agent 运行时做实验。

每个 Agent 都应该有自己的 memory、workspace、session、configuration、runtime home、login state 和 lifecycle。

用户不应该手动创建容器、编写启动脚本、复制 API key、拆分数据目录，或者记住哪个进程属于哪个 Agent。

---

## 仓库定位

当前仓库聚焦于：

```text
开放创意 + MVP 规格 + Prompt Kit + 可选参考实现
```

它刻意不强制规定唯一的实现流程。

你可以：

- 从空仓库开始；
- 从自己的 fork 开始；
- 只把这个仓库当作产品 brief；
- 使用任意分支命名方式；
- 使用任意 Coding Agent；
- 使用合理的任意技术栈；
- 创建自己的 prompt 变体。

真正重要的是保留 AgentBox 的产品意图、MVP 边界和安全约束。

---

## 哪些东西应该保持一致

一个 AgentBox 类实现应该保持这些原则：

- 单机优先；
- 多个彼此隔离、长期运行的 Agent 实例；
- 一个 owner 可以拥有多个 agent；
- MVP 中一个 agent 只属于一个 owner；
- 每个 agent 有独立的 runtime home、memory、sessions、workspace 和 config；
- 支持平台级共享 model provider / key，让最终用户不用自己管理模型凭据；
- 基于容器或 sandbox 的隔离；
- 推荐 Podman / rootless-first runtime；
- 不依赖 Docker Desktop；
- 不把宿主机 home 目录挂载进 agent 容器；
- 不把其他 agent 的数据目录挂载进当前 agent 容器；
- 不把 Docker 或 Podman socket 挂载进 agent 容器；
- 不通过 CLI、API、日志或 UI 泄漏 secret value。

---

## 哪些东西可以改

欢迎自由改造：

- 实现语言；
- Web 框架；
- 数据库；
- UI 设计；
- 分支流程；
- Prompt 风格；
- Coding Agent；
- Runtime driver；
- 打包方式；
- 部署模型；
- milestone 顺序，只要 MVP 意图保持清晰。

建议技术栈只是建议：

- backend: Python + FastAPI；
- CLI: Typer；
- database: SQLite；
- frontend: React + Vite + TypeScript；
- runtime: Podman / rootless Podman。

其他技术栈也可以。

---

## 建议仓库结构

```text
docs/
  vision.md                  # 产品创意和问题背景
  mvp-spec.md                # MVP 必要行为
  architecture-principles.md # 运行时和隔离模型
  safety-rules.md            # 不可妥协的安全规则
  acceptance-demo.md         # 有用实现的验收 Demo

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

## 建议 Milestones

这些 milestones 是指导，不是强制分支计划。

1. **产品规格和 Prompt Kit**
   - 澄清想法、MVP、安全规则和验收 Demo；
   - 创建可复用的 Coding Agent prompts。

2. **核心领域模型和 CRUD**
   - owners；
   - agents；
   - platform settings；
   - secret metadata，不泄漏 secret value；
   - CLI/API 可选。

3. **Podman runtime driver**
   - build/start/stop/restart/remove containers；
   - inspect status；
   - logs；
   - exec/shell；
   - mount validation。

4. **Hermes runtime P0**
   - 每个 agent 独立 `HERMES_HOME`；
   - 生成 config 和 env；
   - 注入共享 model key；
   - 以 `hermes gateway run` 作为长期运行命令。

5. **Lifecycle management**
   - backup；
   - restore；
   - reset；
   - diagnose；
   - upgrade。

6. **Web console**
   - login；
   - dashboard；
   - owners；
   - agents；
   - logs；
   - settings；
   - backups。

7. **Additional runtimes**
   - OpenClaw；
   - coding-agent wrappers；
   - custom MCP agents；
   - 其他 Agent frameworks。

---

## Prompt Kit 快速开始

从 `prompts/` 中选择一个 prompt，粘贴给你喜欢的 Coding Agent。

如果是新实现，从这里开始：

```text
prompts/00-build-from-scratch.md
```

如果已有核心 CRUD，下一步可以继续：

```text
prompts/02-podman-runtime.md
```

你可以自由修改这些 prompts。

---

## MVP 非目标

AgentBox MVP 不应该一开始就变成：

- SaaS 多租户平台；
- Kubernetes 编排系统；
- 企业级 RBAC / 审计套件；
- Marketplace；
- serverless / Knative 唤醒系统；
- WeChat、Telegram、Feishu、Slack 等消息网关的替代品；
- 依赖 Docker Desktop 的工具；
- 把宿主机 home 目录或容器 socket 暴露给 Agent 的系统。

这些可以是未来实验，但不应该主导第一个有用版本。

---

## 当前状态

这个仓库已经被重新定位为产品创意、MVP 规格和 Prompt Kit。

早期实现代码已经从 main 分支移除，以保持项目开放、可二创、适合 Coding Agent 使用。

未来贡献者可以在清晰命名的目录下添加参考实现，例如：

```text
reference-implementations/python-fastapi/
```

这样不会把整个仓库重新绑定成唯一固定实现。

---

## License

MIT. See [LICENSE](LICENSE) if present. If a generated implementation uses this repository as input, keep the license and attribution appropriate for your project.
