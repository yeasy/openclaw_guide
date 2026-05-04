## 附录E：命令速查手册

本附录汇总 OpenClaw 的终端 CLI 命令与聊天斜杠命令，供日常操作时快速查阅。命令参数可能随版本演进，建议以 `openclaw <命令> --help` 的实际输出为准。

### E.1 基础操作与服务管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw --version` | 查看当前版本号 | [2.1](../02_setup/2.1_requirements.md) |
| `openclaw --help` | 查看所有可用命令与用法 | — |
| `openclaw tui` | 打开终端交互对话界面 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw dashboard` | 打开网页控制台（Dashboard） | [3.1](../03_minimal_loop/3.1_control_ui_webchat.md) |
| `openclaw gateway restart` | 重启网关服务（改完配置后常用） | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw gateway stop` | 停止网关服务 | — |
| `openclaw update` | 更新到最新版本 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --channel stable` | 切换到稳定版通道并更新 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --channel beta` | 切换到测试版通道并更新 | [2.2](../02_setup/2.2_installation.md) |

### E.2 安装、初始化与配置

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw setup` | 初始化配置文件、工作区与会话目录 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw onboard` | 启动交互式配置向导 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw setup --wizard` | 从 `setup` 入口进入交互式向导 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw onboard --install-daemon` | 配置向导 + 安装为系统后台服务 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw configure` | 重新进入配置向导（可随时修改设置） | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw config file` | 查看当前配置文件路径 | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw config get <路径>` | 读取指定配置项的当前值 | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw config set <路径> <值>` | 非交互式更新指定配置项 | [4.1](../04_config_models/4.1_config_system.md) |

### E.3 诊断与排障

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw doctor` | 全面健康检查（配置、端口、依赖） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw doctor --repair` | 健康检查 + 应用推荐修复（`--fix` 为别名） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw health --json` | 健康探针（适合自动化） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw status` | 查看运行状态（Gateway 是否在线、端口等） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw status --deep` | 详细状态（含网关健康探测） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw logs` | 查看最近日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw logs --follow --json` | 实时跟踪结构化日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw security audit` | 安全基线审计（谁能对话、在哪执行、能触及什么） | [8.5](../08_automation_ops/8.5_security_baseline.md) |
| `openclaw security audit --deep` | 深度安全审计 | [8.5](../08_automation_ops/8.5_security_baseline.md) |
| `openclaw security audit --fix` | 安全审计 + 自动修复 | [8.5](../08_automation_ops/8.5_security_baseline.md) |

> 遇到问题时的推荐排查顺序：`doctor` → `logs` → `status` → `gateway restart` → `doctor --repair`。旧资料里常见的 `doctor --fix` 仍会在部分迁移/兼容文档中出现；实际以本地 `openclaw doctor --help` 为准。详见[附录C](troubleshooting_checklist.md)。

### E.4 模型管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw models list` | 列出所有已配置的模型 | [4.3](../04_config_models/4.3_model_selection.md) |
| `openclaw models set <供应商/模型名>` | 切换默认模型 | [4.3](../04_config_models/4.3_model_selection.md) |
| `openclaw models status --check` | 模型接口连通性验证 | [4.2](../04_config_models/4.2_provider_access.md) |
| `openclaw models auth add --provider <供应商>` | 交互式添加供应商认证档案 | [4.2](../04_config_models/4.2_provider_access.md) |
| `openclaw models auth setup-token --provider <供应商>` | 为指定供应商生成 Token 录入流程 | [4.2](../04_config_models/4.2_provider_access.md) |
| `openclaw models auth paste-token --provider <供应商>` | 粘贴 API Token 认证 | [4.2](../04_config_models/4.2_provider_access.md) |

### E.5 渠道管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw channels list` | 列出已配置的渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels status --probe` | 主动探测渠道链路状态 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw channels capabilities` | 渠道能力、配置与联调入口 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw channels add` | 添加新渠道（交互式向导） | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels add --channel telegram --token <TOKEN>` | 非交互式添加 Telegram 渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels add --channel feishu` | 添加飞书渠道 | [7.2](../07_multi_agent/7.2_lark_integration.md) |
| `openclaw channels remove --channel <名称>` | 移除渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels logs` | 查看渠道日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw channels login` | 登录渠道（如 WhatsApp Web） | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels logout` | 登出渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |

常见渠道类型包括：`whatsapp`、`telegram`、`discord`、`slack`、`googlechat`、`signal`、`bluebubbles`、`irc`、`matrix`、`nextcloud-talk`、`nostr`、`qqbot`、`synology-chat`、`twitch`、`openclaw-weixin`、`zalo`、`zalouser`、`feishu`、`mattermost`、`msteams`。`webchat` 更适合作为内部 UI 渠道理解，而不是常规出站 channel 类型；`imessage` 目前属于 legacy 路径。完整列表以当前版本 CLI 与官方渠道文档为准。

### E.6 插件与技能

**插件管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw plugins list` | 列出所有插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins install <插件名>` | 安装插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins enable <插件名>` | 启用插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins disable <插件名>` | 禁用插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins inspect <插件名>` | 查看单个插件详情与来源 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins doctor` | 检查插件加载错误 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |

**技能管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw skills search <关键词>` | 在技能仓库中搜索技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `openclaw skills list` | 列出已安装的技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `openclaw skills install <技能名>` | 安装技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |

### E.7 网关管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw gateway start` | 启动网关 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway --port <端口>` | 指定端口启动 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway --verbose` | 启动并显示详细日志 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway status` | 查看网关的当前状态 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway restart` | 重启网关 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway --token <token>` | 带 token 启动 | [9.3](../09_gateway_protocol/9.3_ws_handshake.md) |

### E.8 沙箱与浏览器

**沙箱管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw sandbox explain` | 查看当前沙箱配置状态 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox explain --json` | JSON 格式查看沙箱配置 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox list` | 列出所有沙箱容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox list --browser` | 只列出浏览器容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox recreate --all` | 重建所有容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox recreate --all --force` | 强制重建（跳过确认） | [11.4](../11_reliability_security/11.4_guardrails.md) |

**浏览器控制**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw browser open <URL>` | 打开网页 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser snapshot` | 截取当前页面快照 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser screenshot` | 截图 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser click <元素>` | 点击页面元素 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser type <元素> <文字>` | 在输入框中输入文字 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser stop` | 停止浏览器服务 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser close <tab>` | 关闭指定标签页 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser console` | 查看浏览器控制台日志 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |

### E.9 消息与配对

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw message send --target <号码> --message "内容"` | 向指定目标发送消息 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw agent --message "任务内容"` | 直接给 Agent 发任务 | [7.3](../07_multi_agent/7.3_routing_basics.md) |
| `openclaw agent --message "任务" --thinking high` | 发任务（高思考深度） | [7.3](../07_multi_agent/7.3_routing_basics.md) |
| `openclaw pairing approve <渠道> <配对码>` | 批准私聊配对码 | [9.5](../09_gateway_protocol/9.5_pairing_trust.md) |

### E.10 聊天斜杠命令

以下命令在 OpenClaw 的聊天窗口中使用（WebChat、飞书、Telegram 等通用）。

**会话管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/new` | 开始新会话（清除上下文） | [6.1](../06_context_memory/6.1_sessions.md) |
| `/new <任务描述>` | 开始新会话并附带任务 | [6.1](../06_context_memory/6.1_sessions.md) |
| `/compact` | 压缩当前上下文（保留要点，减少 Token） | [6.4](../06_context_memory/6.4_compaction_pruning.md) |
| `/btw <问题>` | 针对当前上下文的旁路提问，不影响后续会话上下文 | — |
| `/status` | 查看当前会话状态（Token 用量、模型等） | [6.1](../06_context_memory/6.1_sessions.md) |
| `/help` 或 `/commands` | 查看所有可用斜杠命令 | — |

**模型切换**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/model` | 查看当前使用的模型 | [4.3](../04_config_models/4.3_model_selection.md) |
| `/model <模型名>` | 切换到指定模型 | [4.3](../04_config_models/4.3_model_selection.md) |

**任务、上下文与导出**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/tasks` | 查看当前会话相关的后台任务 | [7.4](../07_multi_agent/7.4_collaboration_patterns.md) |
| `/context [list\|detail\|json]` | 查看当前会话的上下文组成 | [6.2](../06_context_memory/6.2_context_building.md) |
| `/export-session [path]` | 导出当前会话 HTML 记录 | [6.1](../06_context_memory/6.1_sessions.md) |

**工具与执行控制**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/approve <id> <decision>` | 处理待确认的审批请求 | [5.2](../05_tools_skills/5.2_tool_policy.md) |
| `/allowlist` | 查看或维护会话允许名单 | [5.2](../05_tools_skills/5.2_tool_policy.md) |
| `/usage [off\|tokens\|full]` | 控制每条回复是否附带用量摘要 | [14.3](../14_performance_cost/14.3_usage_budget.md) |

**技能、插件与记忆**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/skill <名称> [输入]` | 按名称运行指定技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `/plugins install\|enable\|disable` | 安装或启停插件（按当前权限与配置门控执行） | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `/plugin ...` | `/plugins` 的别名 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |

**信息查询**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/usage cost` | 查看当前会话的本地成本摘要 | [14.3](../14_performance_cost/14.3_usage_budget.md) |
| `openclaw --version` | 查看 CLI 版本信息 | — |
| `openclaw gateway status` | 测试网关连接和运行状态 | [2.4](../02_setup/2.4_gateway_service.md) |

### E.11 关键文件路径速查

| 路径 | 说明 | 关联章节 |
|---|---|---|
| `~/.openclaw/openclaw.json` | 主配置文件 | [4.1](../04_config_models/4.1_config_system.md) |
| `~/.openclaw/workspace/` | 默认工作区（含引导文件） | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/AGENTS.md` | 工作区主页与启动清单 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/SOUL.md` | 智能体人格定义 | [3.3.4](../03_minimal_loop/3.3_agent_persona.md) |
| `~/.openclaw/workspace/USER.md` | 用户偏好与画像 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/IDENTITY.md` | 智能体元数据（名称、形象） | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/TOOLS.md` | 环境级工具备忘 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/HEARTBEAT.md` | 心跳巡检清单 | [8.3](../08_automation_ops/8.3_heartbeat.md) |
| `~/.openclaw/workspace/BOOT.md` | 仅在启用对应 startup hook 时使用的启动脚本 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/BOOTSTRAP.md` | 首次运行入职脚本 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/MEMORY.md` | 可选长期记忆索引 | [6.3](../06_context_memory/6.3_memory_mechanism.md) |
| `~/.openclaw/workspace/memory/` | 记忆或 hook 写入目录，不等于每轮自动加载 | [6.3](../06_context_memory/6.3_memory_mechanism.md) |
| `~/.openclaw/workspace/skills/` | 当前工作区技能目录；`openclaw skills install` 默认写到这里 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.openclaw/workspace/.agents/skills/` | 工作区私有 Agent skills 目录 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.openclaw/workspace/canvas/` | 节点 UI 或可视化资源 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/skills/` | 本地 override / 共享技能目录（非当前 CLI 默认安装目标） | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.agents/skills/` | 用户级共享 Agent skills 目录 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.openclaw/agents/` | Agent 数据目录 | — |
| `~/.openclaw/cron/jobs.json` | 定时任务定义存储 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `~/.openclaw/agents/<ID>/sessions/` | 会话记录 | [6.1](../06_context_memory/6.1_sessions.md) |

> Windows 用户注意：`~` 等于 `%USERPROFILE%`，即 `C:\Users\<你的用户名>`。
