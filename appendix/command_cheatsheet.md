## 附录E：命令速查手册

本附录汇总 OpenClaw 的终端 CLI 命令与聊天斜杠命令，供日常操作时快速查阅。命令参数可能随版本演进，建议以 `openclaw <命令> --help` 的实际输出为准。

> 本表覆盖正文各章用到的 CLI 命令。两类入口刻意不收录：一是正文已明确标注为**尚不稳定**的命令（如 `openclaw invoke`，见 [12.3](../12_extension_engineering/12.3_testing_debugging.md)）；二是 `/subagents`、`/codex` 这类正文只在特定语境提到、其子命令形态需以官方文档和本地 `--help` 为准的入口。另需区分：[3.1](../03_minimal_loop/3.1_control_ui_webchat.md) 里的 `/chat`、`/overview`、`/sessions`、`/cron`、`/agents` 等是 Control UI 的**页面路由**，不是聊天斜杠命令。

### E.1 基础操作与服务管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw --version` | 查看当前版本号 | [2.1](../02_setup/2.1_requirements.md) |
| `openclaw --help` | 查看所有可用命令与用法 | — |
| `openclaw tui` | 打开终端交互对话界面 | [2.3](../02_setup/2.3_onboarding.md) |
| `openclaw dashboard` | 打开网页控制台（Dashboard） | [3.1](../03_minimal_loop/3.1_control_ui_webchat.md) |
| `openclaw gateway restart` | 重启网关服务（改完配置后常用） | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw gateway stop` | 停止网关服务；不要用作“重启”的前半步 | — |
| `openclaw update` | 更新到最新版本 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update status` | 查看当前安装与更新状态 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --dry-run` | 预演更新，不实际安装 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --channel stable` | 切换到稳定版通道并更新 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --channel beta` | 切换到测试版通道并更新 | [2.2](../02_setup/2.2_installation.md) |
| `openclaw update --channel dev` | 切换到开发通道并更新 | [2.2](../02_setup/2.2_installation.md) |

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
| `openclaw config unset <路径>` | 删除指定配置项（迁移旧字段时常用） | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw config validate` | 校验配置文件结构与字段合法性 | [4.1](../04_config_models/4.1_config_system.md) |
| `openclaw config schema` | 查看当前版本支持的配置 schema | [4.1](../04_config_models/4.1_config_system.md) |

### E.3 诊断与排障

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw doctor` | 全面健康检查（配置、端口、依赖） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw doctor --repair` | 健康检查 + 应用推荐修复（`--fix` 为别名） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw health --json` | 健康探针（适合自动化） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw status` | 查看运行状态（Gateway 是否在线、端口等） | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw status --deep` | 详细状态与渠道 live probe | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw status --usage` | 供应商配额/窗口快照；不等同于成本趋势报表 | [14.3](../14_performance_cost/14.3_usage_budget.md) |
| `openclaw status --all` | 一次性输出各状态分组的汇总 | [15.1](../15_troubleshooting_trees/15.1_diagnostic_decision_trees.md) |
| `openclaw logs` | 查看最近日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw logs --follow --json` | 实时跟踪结构化日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw logs --limit <N> --json` | 取日志快照证据；排障清单优先用它而不是 `--follow` | [附录C](troubleshooting_checklist.md) |
| `openclaw gateway probe` | 主动探测 Gateway 可达性 | [15.1](../15_troubleshooting_trees/15.1_diagnostic_decision_trees.md) |
| `openclaw gateway stability --json` | 网关稳定性快照（崩溃、重启、资源饱和） | [15.2](../15_troubleshooting_trees/15.2_high_concurrency_diagnosis.md) |
| `openclaw gateway stability --bundle latest --export` | 导出最近一次稳定性事件包 | [15.2](../15_troubleshooting_trees/15.2_high_concurrency_diagnosis.md) |
| `openclaw gateway diagnostics export --json` | 导出受控诊断包用于提 Issue；聊天内等价入口为 `/diagnostics` | [附录C](troubleshooting_checklist.md) |
| `openclaw proxy validate` | 校验托管代理运行时路径（`proxy.enabled` / `proxy.proxyUrl` / `OPENCLAW_PROXY_URL`） | [附录H](env_check.md) |
| `openclaw security audit` | 安全基线审计（谁能对话、在哪执行、能触及什么） | [8.5](../08_automation_ops/8.5_security_baseline.md) |
| `openclaw security audit --deep` | 深度安全审计（live Gateway probes + 插件安全 collector） | [8.5](../08_automation_ops/8.5_security_baseline.md) |
| `openclaw security audit --fix` | 安全审计 + 自动修复 | [8.5](../08_automation_ops/8.5_security_baseline.md) |

> 遇到问题时的推荐排查顺序：`doctor` → `logs` → `status` → `gateway restart` → `doctor --repair`。旧资料里常见的 `doctor --fix` 仍会在部分迁移/兼容文档中出现；实际以本地 `openclaw doctor --help` 为准。详见[附录C](troubleshooting_checklist.md)。

### E.4 模型管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw models list` | 列出所有已配置的模型 | [4.3](../04_config_models/4.3_model_selection.md) |
| `openclaw models set <供应商/模型名>` | 切换默认模型 | [4.3](../04_config_models/4.3_model_selection.md) |
| `openclaw models status` | 检查模型配置与认证状态 | [4.2](../04_config_models/4.2_provider_access.md) |
| `openclaw models status --probe` | live provider 认证探针 | [4.2](../04_config_models/4.2_provider_access.md) |
| `openclaw models auth add` | 交互式添加供应商认证档案 | [4.2](../04_config_models/4.2_provider_access.md) |
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
| `openclaw channels add` | 添加/绑定飞书渠道（向导中选择 Feishu） | [7.2](../07_multi_agent/7.2_lark_integration.md) |
| `openclaw channels remove --channel <名称>` | 移除渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels logs` | 查看渠道日志 | [3.2](../03_minimal_loop/3.2_diagnostics.md) |
| `openclaw channels login` | 登录渠道（如 WhatsApp Web） | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw channels logout` | 登出渠道 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |

常见渠道类型包括：`whatsapp`、`telegram`、`discord`、`slack`、`googlechat`、`signal`、`imessage`、`irc`、`matrix`、`nextcloud-talk`、`nostr`、`qqbot`、`synology-chat`、`twitch`、`openclaw-weixin`、`zalo`、`zalouser`、`feishu`、`mattermost`、`msteams`。`webchat` 更适合作为内部 UI 渠道理解，而不是常规出站 channel 类型；BlueBubbles 已迁移为 iMessage 路径。完整列表以当前版本 CLI 与官方渠道文档为准。

### E.6 插件与技能

**插件管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw plugins list` | 列出所有插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins install <path-or-spec>` | 按 npm、ClawHub、git、本地路径或 marketplace spec 安装插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins enable <插件名>` | 启用插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins disable <插件名>` | 禁用插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins inspect <插件名>` | 查看单个插件详情与来源 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins inspect <id> --runtime --json` | 查看插件运行时状态（是否加载、启用、健康） | [5.1](../05_tools_skills/5.1_tool_inventory.md) |
| `openclaw plugins update <id-or-npm-spec>` | 更新单个已追踪插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins update --all` | 更新全部已追踪插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins marketplace list <市场名>` | 列出指定市场中的可用插件 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |
| `openclaw plugins doctor` | 检查插件加载错误 | [12.1](../12_extension_engineering/12.1_plugin_architecture.md) |

**技能管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw skills search <关键词>` | 在技能仓库中搜索技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `openclaw skills list` | 列出已安装的技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `openclaw skills install <技能名>` | 安装技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `openclaw skills update <技能名>` / `openclaw skills update --all` | 更新单个技能或当前工作区内所有可追踪 ClawHub 技能 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |

### E.7 网关管理

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw gateway start` | 启动网关 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway run --port <端口>` | 指定端口前台启动 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway run --verbose` | 前台启动并显示详细日志 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway status` | 查看网关的当前状态 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway status --deep --require-rpc` | 确认 Gateway runtime 可用（工具清单取证时的运行时证据） | [5.1](../05_tools_skills/5.1_tool_inventory.md) |
| `openclaw gateway install` | 安装托管 Gateway 服务 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway uninstall` | 卸载托管 Gateway 服务 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway restart` | 重启网关 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway stop --disable` | macOS 上停止并持久禁用 LaunchAgent 自动启动 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw gateway run --token <token>` | 带 token 前台启动 | [9.3](../09_gateway_protocol/9.3_ws_handshake.md) |
| `openclaw daemon status` | 服务状态别名入口 | [2.4](../02_setup/2.4_gateway_service.md) |
| `openclaw daemon install/start/stop/restart/uninstall` | 服务生命周期别名入口 | [2.4](../02_setup/2.4_gateway_service.md) |

> macOS 上需要重启托管 Gateway 时，优先使用 `openclaw gateway restart`。不要把 `gateway stop` + `gateway start` 当作等价重启流程。

### E.8 沙箱与浏览器

**沙箱管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw sandbox explain` | 查看当前沙箱配置状态 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox explain --json` | JSON 格式查看沙箱配置 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox list` | 列出所有沙箱容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox list --browser` | 只列出浏览器容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox recreate --all` | 重建所有容器 | [11.4](../11_reliability_security/11.4_guardrails.md) |
| `openclaw sandbox recreate --all --force` | 强制重建（跳过确认；会删除沙箱运行时，远程后端可能删除该 scope 的远程工作区） | [11.4](../11_reliability_security/11.4_guardrails.md) |

**浏览器控制**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw browser status` | 查看浏览器服务与节点状态 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser start` | 启动浏览器服务 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser doctor` | 浏览器链路健康检查 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser open <URL>` | 打开网页 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser snapshot` | 截取当前页面快照 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser screenshot` | 截图 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser click <ref>` | 点击快照中的页面元素 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser type <ref> "文字"` | 在快照引用对应的输入框中输入文字 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser stop` | 停止浏览器服务 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser close <tab>` | 关闭指定标签页 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser console` | 查看浏览器控制台日志 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |
| `openclaw browser evaluate` | 在页面中执行 JavaScript；**可执行任意 JS，存在提示注入风险**，非必要时用 `browser.evaluateEnabled=false` 关闭 | [5.4](../05_tools_skills/5.4_browser_nodes.md) |

### E.9 消息与配对

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw message send --target <号码> --message "内容"` | 向指定目标发送消息 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |
| `openclaw agent --agent <agentId> --message "任务内容"` | 直接给指定 Agent 发任务 | [7.3](../07_multi_agent/7.3_routing_basics.md) |
| `openclaw agent --agent <agentId> --message "任务" --thinking high` | 给指定 Agent 发任务（高思考深度） | [7.3](../07_multi_agent/7.3_routing_basics.md) |
| `openclaw agents list` | 列出所有智能体及其启用状态 | [15.1](../15_troubleshooting_trees/15.1_diagnostic_decision_trees.md) |
| `openclaw agents list --bindings` | 列出智能体并附带路由绑定 | [7.4](../07_multi_agent/7.4_collaboration_patterns.md) |
| `openclaw agents bindings` | 查看所有智能体的路由绑定 | [7.3](../07_multi_agent/7.3_routing_basics.md) |
| `openclaw agents bindings --agent <agentId>` | 查看指定智能体的路由绑定详情 | [7.3](../07_multi_agent/7.3_routing_basics.md) |

**渠道私聊配对**（配对码走 `pairing`）

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw pairing list <渠道>` | 列出该渠道的待批准配对请求 | [3.4](../03_minimal_loop/3.4_pairing_groups.md) |
| `openclaw pairing approve <渠道> <配对码>` | 批准私聊配对码 | [9.5](../09_gateway_protocol/9.5_pairing_trust.md) |
| `openclaw pairing approve <渠道> <配对码> --notify` | 批准并通知对方 | [7.1](../07_multi_agent/7.1_telegram_whatsapp.md) |

**Control UI、节点与设备配对**（走 `devices`，与上面的渠道配对是两条不同链路）

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw devices list` | 查看设备与待批准请求；`requestId` 会随重试或重开页面变化，批准前应重新执行 | [3.1](../03_minimal_loop/3.1_control_ui_webchat.md) |
| `openclaw devices approve <requestId>` | 批准待配对设备 | [3.1](../03_minimal_loop/3.1_control_ui_webchat.md) |
| `openclaw devices remove <deviceId>` | 移除已配对设备 | [3.4](../03_minimal_loop/3.4_pairing_groups.md) |
| `openclaw devices revoke --device <deviceId> --role <role>` | 回收设备的指定角色权限 | [3.4](../03_minimal_loop/3.4_pairing_groups.md) |

### E.10 自动化与运维

**定时任务（Cron）**

作业创建需要先区分 payload 类型：主会话任务用 `--system-event`（通常配合 `--session main`），隔离任务用 `--message`（通常配合 `--session isolated`）。不带时区的 `--at` 按 UTC 解释，要按本地墙上时间应显式传 `--tz <IANA 时区>`。

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw cron add --name <名称> --cron "<表达式>" --session main --system-event "<内容>" --wake now` | 创建主会话定时作业并立即唤醒心跳处理 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron add --name <名称> --at "<时间>" --session isolated --message "<内容>" --announce` | 创建一次性隔离作业并主动投递结果 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron list` | 查看所有已注册作业及下次触发时间 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron status` | 查看 cron 调度器健康度 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron show <jobId>` | 查看单个作业详情 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron run <jobId>` | 默认强制排队执行并立即返回；加 `--due` 才保持“到期才执行” | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron enable <jobId>` / `openclaw cron disable <jobId>` | 启用 / 禁用指定作业 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron edit <jobId> --no-deliver` | 改写作业投递行为（隔离作业默认 `announce` 回退投递） | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron runs --id <jobId>` | 查看执行历史；`cron run` 返回只代表已入队，是否真的运行要用它对账 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `openclaw cron remove <jobId>` | 移除指定作业（`rm`/`delete` 等别名以当前 CLI 为准） | [8.2](../08_automation_ops/8.2_cron_jobs.md) |

**心跳与系统事件**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw system event --text "<内容>" --mode now` | 注入系统事件并立即唤醒心跳 | [8.3](../08_automation_ops/8.3_heartbeat.md) |
| `openclaw system event --text "<内容>" --mode next-heartbeat` | 注入系统事件，等下一个心跳周期再处理 | [8.3](../08_automation_ops/8.3_heartbeat.md) |

**Hook 管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw hooks list` | 列出可发现的 Hook 及启用状态 | [8.1](../08_automation_ops/8.1_hooks.md) |
| `openclaw hooks info <hook>` | 查看单个 Hook 的详情与来源 | [8.1](../08_automation_ops/8.1_hooks.md) |
| `openclaw hooks check` | 检查 Hook 定义与加载问题 | [8.1](../08_automation_ops/8.1_hooks.md) |
| `openclaw hooks enable <hook>` / `openclaw hooks disable <hook>` | 启用 / 禁用指定 Hook | [8.1](../08_automation_ops/8.1_hooks.md) |

**凭据管线（Secrets）**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw secrets audit` | 审计凭据引用与依赖 | [8.5](../08_automation_ops/8.5_security_baseline.md) |
| `openclaw secrets audit --check` | 迁移前的凭据存储体检 | [附录F](version_mapping.md) |
| `openclaw secrets configure` | 交互式配置 secrets provider 与 `SecretRef` | [附录F](version_mapping.md) |
| `openclaw secrets apply --from <plan.json> --dry-run` | 预演凭据变更计划 | [附录F](version_mapping.md) |
| `openclaw secrets apply --from <plan.json>` | 应用凭据变更计划 | [附录F](version_mapping.md) |
| `openclaw secrets reload` | 重新加载凭据，不重启 Gateway | [8.5](../08_automation_ops/8.5_security_baseline.md) |

**会话维护与成本**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `openclaw sessions cleanup --dry-run` | 预览将被清理的过期会话，不实际删除 | [14.3](../14_performance_cost/14.3_usage_budget.md) |
| `openclaw sessions cleanup --enforce` | 按 `session.maintenance.pruneAfter` / `maxEntries` 实际执行清理 | [14.3](../14_performance_cost/14.3_usage_budget.md) |
| `openclaw gateway usage-cost` | transcript-backed 的 CLI 成本摘要 | [14.1](../14_performance_cost/14.1_token_context_cost.md) |

> 凭据与迁移类命令的名称、参数在不同版本可能有差异（书中 8.5 与附录 F 均已就此提示）。执行失败时先用 `openclaw --help` 或 `openclaw <命令> --help` 确认当前语法，不要照抄旧文档。

### E.11 聊天斜杠命令

以下命令在 OpenClaw 的聊天窗口中使用（Control UI chat、飞书、Telegram 等通用）。

**会话管理**

| 命令 | 说明 | 关联章节 |
|---|---|---|
| `/new` | 开始新会话（清除上下文） | [6.1](../06_context_memory/6.1_sessions.md) |
| `/new [model/任务描述]` | 开始新会话；参数优先按模型解析，无法匹配时作为首条消息 | [6.1](../06_context_memory/6.1_sessions.md) |
| `/reset` | 与 `/new` 同属重置入口：为同一 `sessionKey` 建新 `sessionId`，磁盘上的记忆文件不受影响 | [6.1](../06_context_memory/6.1_sessions.md) |
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
| `/tools` / `/tools verbose` | 查看当前 session 实际可达的工具（运行时证据，优先于配置推断） | [5.1](../05_tools_skills/5.1_tool_inventory.md) |
| `/queue collect [debounce:<时长>] [cap:<条数>] [drop:<策略>]` | 按会话临时调整消息合并队列行为 | [7.4](../07_multi_agent/7.4_collaboration_patterns.md) |
| `/queue reset` | 恢复队列的默认行为 | [7.4](../07_multi_agent/7.4_collaboration_patterns.md) |
| `/trace on` | 打开工具与插件 trace，诊断信息进入会话与结构化日志 | [14.2](../14_performance_cost/14.2_latency_throughput.md) |
| `/diagnostics [补充说明]` | 在聊天窗口导出受控诊断包（等价于 `openclaw gateway diagnostics export`） | [附录C](troubleshooting_checklist.md) |
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

### E.12 关键文件路径速查

下表使用默认工作区路径 `~/.openclaw/workspace/`。如果配置了 `OPENCLAW_PROFILE` 或自定义 `agents.defaults.workspace` / `agent.workspace`，请把这些路径替换为当前实际 agent workspace。

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
| `~/.openclaw/workspace/BOOT.md` | 非默认创建；仅在文件存在且启用 bundled `boot-md` hook 时执行 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/BOOTSTRAP.md` | 首次运行入职脚本 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/workspace/MEMORY.md` | 可选长期记忆索引 | [6.3](../06_context_memory/6.3_memory_mechanism.md) |
| `~/.openclaw/workspace/memory/` | 记忆或 hook 写入目录，不等于每轮自动加载 | [6.3](../06_context_memory/6.3_memory_mechanism.md) |
| `<workspace>/skills/` | 当前工作区技能目录；`openclaw skills install` 默认写到这里 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `<workspace>/.agents/skills/` | 工作区私有 Agent skills 目录 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.openclaw/workspace/canvas/` | 节点 UI 或可视化资源 | [2.3.4](../02_setup/2.3_onboarding.md) |
| `~/.openclaw/skills/` | 本地 override / 共享技能目录（非当前 CLI 默认安装目标） | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.agents/skills/` | 用户级共享 Agent skills 目录 | [5.3](../05_tools_skills/5.3_skills_plugins.md) |
| `~/.openclaw/agents/` | Agent 数据目录 | — |
| `~/.openclaw/cron/jobs.json` | 定时任务定义存储 | [8.2](../08_automation_ops/8.2_cron_jobs.md) |
| `~/.openclaw/agents/<ID>/sessions/` | 会话记录 | [6.1](../06_context_memory/6.1_sessions.md) |

> Windows 用户注意：`~` 等于 `%USERPROFILE%`，即 `C:\Users\<你的用户名>`。
