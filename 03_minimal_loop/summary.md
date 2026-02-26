## 3.5 本章小结

第三章的目标是建立“本地最小闭环基准线”：在不引入外部渠道变量的前提下，验证主链路可用、可观测、可复验，并为后续的配置调优与扩展落地提供稳定的参照系。

### 3.5.1 关键设计原则沉淀

完成本章后，应形成以下关键结论：

- 基准线优先：先在 Dashboard/WebChat 跑通固定用例，再扩展渠道与能力，避免变量叠加导致问题难复现。
- 指令是契约：初始指令（instructions）要写成可检查条款（目标/边界/输出结构），并配合日志回放验证其生效。
- 入口先收敛：配对、群聊门控与允许列表用于把触发面压到可控范围；高风险能力仍需工具策略兜底。
- 排障看顺序：先 `health/status`，再看渠道与模型可用性，最后回看结构化日志，避免先改提示词掩盖根因。

### 3.5.2 安全与排障自检清单

建议在进入下一章前自检：

- 是否能跑通 3.1 的最小用例，并在 `logs --json` 中定位到对应的请求与 trace？
- 新设备访问是否能完成批准/吊销的操作闭环，并能解释其影响范围？
- 当出现“未响应/未触发/被拦截”时，能否用证据链定位是门控、配对、路由还是工具策略导致？

### 3.5.3 下一步规划预告

[第四章](../04_config_models/README.md)进入配置体系与模型接入：把“能回答”升级为“可控可替换”，并建立可验证的模型选择与故障转移基线。

### 3.5.4 本章参考文献汇总

- Dashboard 命令：https://docs.openclaw.ai/cli/dashboard
- Health 命令：https://docs.openclaw.ai/cli/health
- Web 桌面端：https://docs.openclaw.ai/web/desktop
- Models 命令：https://docs.openclaw.ai/cli/models
- Channels 命令：https://docs.openclaw.ai/cli/channels
- Status 命令：https://docs.openclaw.ai/cli/status
- Doctor 命令：https://docs.openclaw.ai/cli/doctor
- 群组说明：https://docs.openclaw.ai/groups
- 群组消息：https://docs.openclaw.ai/groups/messages
- pairing 命令：https://docs.openclaw.ai/cli/pairing
- Gateway 配置：https://docs.openclaw.ai/gateway/configuration
