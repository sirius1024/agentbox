# AgentBox

[English](README.md)

**AgentBox 是一个开放的产品创意、MVP 规格和 Prompt Kit，用于构建轻量级多 Agent 运行时管理器。**

它帮助构建者使用自己喜欢的 Coding Agent，创建可以在一台个人电脑、家用服务器、实验机器或小团队服务器上运行多个隔离、长期运行 AI Agent 实例的系统。

这个仓库不是一个固定实现。它是面向 Codex、Claude Code、Kimi Code、OpenClaw、Cursor 或其他 Coding Agent 的产品 brief 和 prompt library。

---

## 这个仓库适合谁

AgentBox 适合这些构建者：

- 想在一台机器上运行多个专用 AI Agent；
- 希望每个 Agent 都有独立 memory、sessions、config、workspace 和 runtime home；
- 不想手写容器脚本、到处复制 API key；
- 想让 Coding Agent 生成自己的实现；
- 想 fork、二创或扩展这个产品想法。

如果你想找一个可以直接安装的成品，目前这个仓库还不是。它是用来创建成品的规格和 Prompt Kit。

---

## 快速开始：把 AgentBox 交给你的 Coding Agent

### 1. 选择你的起点

| 当前情况 | 使用这个 Prompt |
| --- | --- |
| 从零开始新实现 | `prompts/00-build-from-scratch.md` |
| 增加核心领域模型和 CRUD | `prompts/01-core-crud.md` |
| 增加 Podman / 容器生命周期 | `prompts/02-podman-runtime.md` |
| 增加 Hermes Agent 运行时 | `prompts/03-hermes-runtime.md` |
| 增加备份、恢复、诊断、升级 | `prompts/04-lifecycle-backup.md` |
| 增加 Web Console | `prompts/05-web-console.md` |
| 需要短通用 Prompt | `prompts/variants/minimal.md` |

### 2. 给 Coding Agent 提供上下文

把整个仓库交给它，或粘贴这些文件：

```text
README.zh-CN.md 或 README.md
docs/vision.md
docs/mvp-spec.md
docs/safety-rules.md
prompts/<selected-prompt>.md
```

### 3. 用直接的任务描述布置工作

```text
Use the AgentBox product spec and prompt kit as input.
Implement the milestone in prompts/<selected-prompt>.md.
Keep the implementation simple and focused.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
Add tests and explain how to run them.
```

也可以用中文：

```text
请基于 AgentBox 的产品规格和 Prompt Kit，完成 prompts/<selected-prompt>.md 中的 milestone。
实现要简单聚焦。
必须遵守 docs/safety-rules.md 中的安全规则。
先不要实现无关的未来功能。
请补充测试，并说明如何运行。
```

你可以使用任何分支流程、技术栈或 Coding Agent。比起精确文件结构，更重要的是安全规则和验收标准。

---

## 需求变化后，如何继续迭代

AgentBox 适合通过 prompt 驱动持续演进。当你修改或新增需求时，不要只对 Coding Agent 说“继续”。应该给它清晰的需求增量。

推荐流程：

1. **先写清楚变化**
   - 更新你自己的 notes、`docs/mvp-spec.md`，或者在 `prompts/` 下创建一个新的 prompt。
   - 变化要小到可以验证。

2. **告诉 Coding Agent 具体变了什么**
   - 新增行为；
   - 修改行为；
   - 删除行为；
   - 哪些约束必须保持不变。

3. **定义验收标准**
   - 哪些命令、测试、UI 流程或 demo 能证明变更成功？

4. **如果产品行为变了，让 Coding Agent 同步更新 docs/prompts**
   - 代码不要和 Prompt Kit 脱节。

5. **按安全规则复核结果**
   - 特别是 mounts、secrets、isolation 和 command execution。

### 需求变更 Prompt 模板

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

这个模板既能约束 Coding Agent，又不会强制一种僵硬的工程流程。

---

## 核心产品想法

AgentBox 希望让个人和小团队托管 Agent 像创建一个托管应用实例一样简单：

1. 创建 owner；
2. 为 owner 创建 agent；
3. 选择 Hermes Agent、OpenClaw 或其他 agent framework 作为 runtime；
4. 在隔离的长期运行容器或 sandbox 中启动 agent；
5. 通过该 runtime 原生接口或 gateway 连接；
6. 监控、修复、备份、恢复、升级。

每个 Agent 都应该拥有自己的：

- runtime home；
- workspace；
- memory 和 sessions；
- configuration；
- login state；
- lifecycle。

---

## 不可妥协的安全规则

任何 AgentBox 类实现都应该保留这些规则：

- 不依赖 Docker Desktop；
- 不把宿主机 home 挂载进 agent runtime；
- 不把宿主机 root 挂载进 agent runtime；
- 不把其他 agent 的数据挂载进当前 agent runtime；
- 不把 Docker 或 Podman socket 挂载进 agent runtime；
- 不通过 CLI、API、日志或 UI 打印 secret value；
- 不用不安全的 shell 字符串拼接来构造 runtime command。

详见 `docs/safety-rules.md`。

---

## 哪些东西应该保持一致

- 单机优先；
- 多个隔离、长期运行的 Agent 实例；
- 一个 owner 可以拥有多个 agent；
- MVP 中一个 agent 只属于一个 owner；
- 支持平台级 model provider/key；
- 基于容器或 sandbox 的隔离；
- 推荐 Podman/rootless-first runtime。

---

## 哪些东西可以改

欢迎自由改造：

- 实现语言；
- 后端框架；
- 数据库；
- UI 设计；
- Coding Agent；
- 分支流程；
- Prompt 风格；
- Runtime driver；
- 部署模型；
- milestone 顺序。

如果你想要一个建议技术栈，可以用：

- Python + FastAPI；
- Typer CLI；
- SQLite；
- React + Vite + TypeScript；
- Podman/rootless Podman。

---

## 仓库结构

```text
docs/
  vision.md                  # 产品创意和问题背景
  mvp-spec.md                # MVP 必要行为
  architecture-principles.md # 运行时和隔离模型
  safety-rules.md            # 不可妥协的安全约束
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

## MVP 非目标

不要让第一个有用实现跑偏到：

- SaaS 多租户；
- Kubernetes 编排；
- 企业级 RBAC / 审计；
- Marketplace；
- serverless / Knative 唤醒；
- 自定义消息网关替代品；
- Docker Desktop 依赖；
- 不安全的宿主机挂载或 secret 泄漏。

这些可以是未来实验，但不应该主导 MVP。

---

## 当前状态

这个仓库目前是产品创意、MVP 规格和 Prompt Kit。

早期实现代码已经从 main 分支移除，以保持项目开放、可二创、适合 Coding Agent 使用。

未来贡献者可以在清晰命名的目录下添加参考实现，例如：

```text
reference-implementations/python-fastapi/
```

---

## License

MIT. See [LICENSE](LICENSE).
