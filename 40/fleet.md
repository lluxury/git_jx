你总结的“Agent 模式 + 编排”完全正确。我逐一核对了官方文档，确认 Kiro、Codex、Copilot 都支持 Subagent 单独绑模型，而 Gemini 目前不支持这个功能。

✅ Kiro：确认支持

官方文档明确说明，每个 Agent 配置里都有 model 字段，用来指定该 Agent 使用哪个 LLM。你可以用 JSON 或 Markdown 格式在 .kiro/agents/ 下创建配置文件，例如：

```markdown
---
name: reviewer
model: claude-sonnet-4-20250514
tools: ["fs_read", "grep"]
---
你是代码审查者...
```

文档甚至直接列出了使用场景：“Different model — use a specific model for certain types of work”。

✅ Codex：确认支持

Codex 的 config.toml 中有明确的 agents.default_subagent_model 字段，官方描述是“Default model for spawned agents”（衍生代理的默认模型）。还支持 agents.<name>.config_file 为每个角色单独指定 TOML 配置文件。

✅ Copilot：确认支持

Copilot 的 Custom Agent 配置中，model 字段的官方说明是：“Model to use when this custom agent runs. If not set, inherits the default model.”（运行此自定义代理时使用的模型。如果未设置，则继承默认模型）。配置文件放在 .github/agents/ 下。

❌ Gemini：不支持 Subagent 单独绑模型

Gemini CLI 确实有 Subagent 机制，支持自动委派和用 @ 语法强制调用特定 Subagent。但官方文档中没有提供为每个 Subagent 单独指定模型的配置字段。

文档中唯一和模型相关的说明是：“Example (forcing a specific model and increasing turns)”，这指的是手动在提示词里指定模型，而不是在 Subagent 配置文件中绑定。Subagent 的配置只涉及 system prompt、工具权限等，不包含 model 字段。

所以 Gemini 只能通过手动切换主会话模型来变相实现，但那就不叫“编排”了，正如你所说。

总结

平台 Subagent 单独绑模型 配置方式
Kiro ✅ 支持 .kiro/agents/ 下的 JSON/MD 文件，model 字段
Codex ✅ 支持 config.toml 的 agents.default_subagent_model + 角色级 config_file
Copilot ✅ 支持 .github/agents/ 下的 .agent.md，model 字段
Gemini ❌ 不支持 Subagent 配置无 model 字段，只能手动切主会话模型




##### g40

多模型分层协作整理文档

整理范围：本话题中关于 Claude Code、Kiro、Codex、Copilot、Gemini 的讨论。
原则：多份相同内容时，取后面生成的版本；所有 Markdown / YAML / TOML / JSON 配置块完整保留。

---

一、通用结论

本质：Agent 模式 + 编排。

拆开就三件事：

1. 定义角色 Agent：规划者、执行者、交互/读写者、部署者。
2. 给每个 Agent 绑不同模型：高级模型绑规划者，中级模型绑执行者，低级模型绑交互/读写者。
3. 用编排层派发和汇总：主 Agent 拆任务，按角色派给对应 Subagent，完成后收摘要。

前提：平台必须支持 Subagent 单独绑模型。如果不支持，就只能手动切模型，不叫编排。

模型分层建议：

· 高级模型：规划、分析、全局把控。
· 中级模型：写代码、实现功能。
· 低级模型：持续交互、接收需求、文件读写、部署命令展示。

---

二、Claude Code

机制

· Subagents：在 .claude/agents/ 下定义，YAML frontmatter 可指定 model 和 tools。
· Hooks：文件编辑后自动触发外部脚本，不消耗模型 token。
· Skills：定义“怎么做”的流程知识。
· Orchestrator-Workers 模式：主会话规划，派发给 Subagent 执行。

配置示例

planner subagent：

```markdown
---
description: 分析需求并输出实施计划，不修改文件
model: opus
tools: [Read, Grep, Glob]
---
你是规划者。分析任务并输出实施步骤，不修改任何文件。
```

implementer subagent：

```markdown
---
description: 按计划实现代码
model: sonnet
tools: [Read, Write, Edit, Bash]
---
你是执行者。按计划实现代码，只修改指定文件。
```

file-worker subagent：

```markdown
---
description: 执行确定性的文件读写和格式转换
model: haiku
tools: [Read, Write]
---
你是文件操作者。按指令批量修改文件，不做任何判断性决策。
```

记忆问题

· 直接切换模型：对话历史保留，但上下文窗口可能静默缩水。
· 分工方式：Subagent 拥有独立上下文窗口，完成后只返回摘要，主线程保留高层上下文。
· 真正持久化靠文件系统：CLAUDE.md、计划文件、子代理产物写入磁盘。
· 关键：规划阶段产出写到磁盘，而不是只留在某个 Subagent 的临时上下文里。

---

三、Kiro

机制

· Crew / Subagents：主 Agent 可派生后台 Agent 并行工作。
· 自定义 Agent：放在 .kiro/agents/（项目级）或 ~/.kiro/agents/（全局），支持 Markdown 或 JSON。
· 模型绑定：每个 Agent 配置里的 model 字段指定该 Agent 使用的 LLM。
· 任务持久化：.kiro/plans/ 计划文件、Notepads、Steering 文件。
· 共享上下文：.kiro/steering/ 下的文件所有 Agent 默认读取。

可用模型与成本倍率（取后面生成的版本）

· 高级（规划）：GPT-5.6 Sol（4.4x）、Claude Opus 5（2.2x）
· 中级（干活）：Claude Sonnet 4.6（1.3x）、GPT-5.6 Luna（1.1x）
· 低级（交互/轻量任务）：Qwen3 Coder Next（0.05x）、MiniMax M2.1（0.15x）

配置示例

executor.md（中级模型执行）：

```markdown
---
name: executor
description: 执行具体的代码编写和文件修改任务
model: claude-sonnet-4.6
tools: [read, write, shell]
---
你是执行者。严格按照收到的任务指令修改代码，不自行扩展范围。
完成后输出变更摘要。
```

planner.json（高级模型规划）：

```json
{
  "name": "planner",
  "description": "分析需求并输出实施计划，不修改文件",
  "tools": ["read", "grep", "glob"],
  "model": "opus"
}
```

implementer.json（中级模型干活）：

```json
{
  "name": "implementer",
  "description": "按计划实现代码",
  "tools": ["read", "write", "shell"],
  "model": "sonnet"
}
```

worker.json（低级模型读写）：

```json
{
  "name": "worker",
  "description": "执行确定性的文件读写和格式转换",
  "tools": ["read", "write"],
  "model": "haiku"
}
```

mcp-reviewer.json（MCP 项目审查）：

```json
{
  "name": "mcp-reviewer",
  "description": "审查 MCP Server 代码的协议合规性",
  "prompt": "你审查 MCP Server 代码。重点关注：工具定义是否符合 MCP 规范、错误处理是否覆盖协议要求的错误码、资源暴露是否只读安全。输出问题列表，不改代码。",
  "tools": ["fs_read", "grep"],
  "model": "claude-sonnet-4",
  "includeMcpJson": true
}
```

Steering 文件示例（.kiro/steering/mcp-context.md）：

```markdown
# MCP Server 项目上下文
- 本项目实现一个 MCP Server，暴露 tool: `query_db`
- 协议版本：2025-06-18
- 传输方式：stdio（本地调试）/ Streamable HTTP（生产）
- 测试命令：`npm test`
- MCP Inspector 调试：`npx @modelcontextprotocol/inspector node dist/server.js`
```

项目级 MCP 配置（.kiro/settings/mcp.json）：

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "node",
      "args": ["dist/server.js"]
    }
  }
}
```

确认

官方文档明确说明每个 Agent 配置里都有 model 字段，用于指定该 Agent 使用哪个 LLM。支持“Different model — use a specific model for certain types of work”。

---

四、Codex

机制

· Orchestrator-Workers / Subagents：主 Agent 分解任务，子 Agent 在独立沙箱中并行执行。
· 模型绑定：config.toml 的 [agents] 段指定子代理默认模型；也可为每个命名角色单独定义 TOML 文件。
· 任务管理：AGENTS.md 定义项目上下文；GitHub Issue 触发任务。
· Auto-review：沙箱中自动运行测试和代码检查。

可用模型（取后面生成的版本）

· 高级：gpt-5.6-sol（旗舰级）
· 低级执行：gpt-5.6-luna（最快、最便宜）
· 免费计划可能只能用 GPT-6 Luna 或 GPT-5.3 Codex Spark。

配置示例

config.toml（全局或项目级）：

```toml
# 主模型：你直接对话时使用的高级模型
model = "gpt-5.6-sol"

# 子代理默认使用的低级模型
[agents]
enabled = true
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "low"
max_concurrent_threads_per_session = 4
```

planner.toml（高级规划）：

```toml
name = "planner"
description = "分析需求，输出计划"
model = "o4-mini"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = "分析任务并输出实施步骤，不修改任何文件。"
```

implementer.toml（中级执行）：

```toml
name = "implementer"
description = "实现代码修改"
model = "gpt-5.3-codex"
sandbox_mode = "workspace-write"
developer_instructions = "按计划实现代码，只修改指定文件。"
```

触发方式

必须显式说 “spawn”：

```text
Spawn a planner subagent to analyze the task and write a plan to /tmp/plan.md.
Then spawn an implementer subagent to execute the plan.
```

已知问题（取后面生成的版本）

Codex CLI 在 v0.144.5 版本存在 bug：子代理的 TOML 模型配置被忽略，子代理会继承父会话的模型。即使 agent 文件里写死了 model = "gpt-5.6-luna"，实际运行时子代理仍可能使用父会话的 gpt-5.6-sol。需要注意版本兼容性。

确认

官方 config.toml 中有 agents.default_subagent_model 字段，描述为“Default model for spawned agents”。支持为每个角色单独指定 TOML 配置文件。

---

五、Copilot

机制

· Custom Agents + /fleet：自定义 Agent 放在 .github/agents/ 下，.agent.md 文件。
· 模型绑定：model 字段指定该 Agent 使用的模型。必须用 slug ID，不能用显示名称。
· /fleet 编排器：自动分析任务、拆解工作项、并行派发给多个子代理。
· Handoff（交接）：可在 Agent 配置中定义交接按钮，手动触发到另一个 Agent。
· 工具权限隔离：通过 tools 字段精确控制每个 Agent 能执行的操作。
· 部署必须人工确认：Copilot CLI 默认手动审批模式，每次工具调用前提示确认。

模型 slug ID 格式

```yaml
# ✅ 正确：slug ID
model: gpt-5.4

# ❌ 错误：显示名称
model: GPT-5.4 (copilot)
```

slug ID 可从 ~/.copilot/config.json 查到。

三层角色配置示例（取后面生成的版本）

交互 Agent（低级模型，负责持续交互）：

```markdown
---
name: interface
description: 与用户持续交互，接收和澄清需求
model: 'Claude Haiku 4.5'
tools: ['read', 'search']
---
你是需求接收者。与用户对话，澄清需求细节，把整理好的任务描述输出给主 Agent。
不要自行修改任何代码。
```

代码实现 Agent（中/高级模型）：

```markdown
---
name: implementer
description: 按需求实现代码
model: 'Claude Sonnet 4.6'
tools: ['read', 'edit', 'runCommands']
---
你是执行者。严格按照收到的任务描述修改代码，不自行扩展范围。
```

规划者 Agent（高级模型）：

```markdown
---
name: planner
description: 分析 MCP 工具需求，输出实施计划
model: 'Claude Opus 4.5'
tools: ['read', 'search']
---
你是规划者。分析用户需求，输出详细的实施步骤和文件清单，不修改任何代码。
```

文件读写者（低级模型）：

```markdown
---
name: file-worker
description: 执行确定性的文件读写和格式转换
model: 'Claude Haiku 4.5'
tools: ['read', 'edit']
---
你是文件操作者。按指令批量修改文件，不做任何判断性决策。
```

部署 Agent（必须人工逐步确认）：

```markdown
---
name: deployer
description: 执行部署操作，必须人工逐步确认
model: 'Claude Sonnet 4.6'
tools: ['read', 'shell(npm run deploy:*)', 'shell(docker push:*)']
---
你是部署执行者。每次执行部署命令前，必须停下来向用户展示即将执行的命令，
等待用户明确确认后才能继续。不要自行决定部署时机。
```

代码交互 Agent 与部署 Agent 的 Handoff 配置：

```markdown
---
name: code-assistant
description: 与用户交互，接收需求并写代码
model: 'gpt-5.4-mini'
tools: ['read', 'edit', 'search']
handoffs:
  - label: "准备部署"
    agent: deployer
    prompt: "代码已就绪，请展示部署命令并等待我确认。"
    send: false
---
你是代码交互者。与用户对话，澄清需求，写代码。写完后询问用户是否进入部署阶段。
```

部署 Agent（独立，只给具体部署命令）：

```markdown
---
name: deployer
description: 执行部署，必须人工逐步确认
model: 'gpt-5.4-mini'
tools:
  - read
  - 'shell(npm run deploy)'
  - 'shell(docker push my-image:*)'
---
你是部署执行者。每次执行命令前，展示完整命令并等待用户明确确认。
```

编排方式

使用 /fleet 命令：

```text
/fleet 使用 planner 制定计划，然后让 implementer 执行
```

```text
/fleet 实现用户登录功能：
1. planner 分析需求并输出计划到 /tmp/plan.md
2. implementer 按计划实现 src/auth/login.ts 并编写单元测试
3. deployer 在测试通过后，执行 npm run deploy 并将结果写入 /tmp/deploy-report.md（依赖 2）
```

部署必须人工确认的机制

· Copilot CLI 默认手动审批模式，每次工具调用前提示确认。
· 部署 Agent 的 tools 只列出具体部署命令，而不是笼统的 shell 权限。
· 支持 --deny-tool，优先级高于 --allow-tool。
· 可用 preToolUse hooks 在工具调用前拦截并强制人工审批。

交互代码和交互部署是否同一个 Agent

推荐拆成两个独立的 Agent：

· 代码 Agent：有 edit 权限，负责写代码。
· 部署 Agent：只有具体 shell(命令) 权限，物理上无法执行 edit。
· 两者可以共用同一个低级模型，但角色定义和工具权限必须分开。
· 通过 handoffs 手动触发交接，send: false 表示不自动发送，预填充提示词等用户确认。

确认

官方文档明确说明 model 字段：“Model to use when this custom agent executes. If unset, inherits the default model.” 支持为每个自定义 Agent 单独绑定模型。

---

六、Gemini

机制

· Gemini CLI 有 Subagent 机制，支持自动委派和用 @ 语法强制调用特定 Subagent。
· 但不支持为每个 Subagent 单独指定模型。官方文档中没有提供 Subagent 配置的 model 字段。
· 唯一和模型相关的说明是“Example (forcing a specific model and increasing turns)”，指手动在提示词里指定模型，而不是在 Subagent 配置文件中绑定。
· Subagent 配置只涉及 system prompt、工具权限等。

结论

Gemini 只能通过手动切换主会话模型来变相实现，不叫“编排”。

---

七、对比总结

平台 Subagent 单独绑模型 配置方式 编排命令/机制
Claude Code ✅ 支持 .claude/agents/ 下 Markdown，YAML frontmatter 中 model Subagents、Hooks、Skills
Kiro ✅ 支持 .kiro/agents/ 下 JSON/MD，model 字段 Crew / Subagents，自动 DAG
Codex ✅ 支持（有版本 bug） config.toml 的 agents.default_subagent_model + 角色 TOML Orchestrator-Workers / Subagents
Copilot ✅ 支持 .github/agents/ 下 .agent.md，model 字段（必须 slug ID） Custom Agents + /fleet
Gemini ❌ 不支持 Subagent 配置无 model 字段 只能手动切主会话模型

最终建议

· 要验证“高级规划、中级干活、低级交互/读写”，Kiro 配置最直观，Copilot 权限控制最细。
· Codex 注意 v0.144.5 的子代理模型继承 bug。
· Gemini 目前不适合做这种分层编排。
· 部署环节必须用工具权限硬隔离 + 人工确认，不能只靠提示词。
