## 16.4 本章小结

本章介绍了 OpenClaw 与主流 AI 生态的集成要点，涵盖 Claude 模型接入、MCP 工具扩展、多智能体协作编排，以及 OpenAI 与本地模型（Ollama）的接入实践。

### 关键结论

- **模型接入的落点在配置**：Claude 模型通过 `provider/model` 标识符接入，大多数场景下 `openclaw onboard` 完成认证后只需指定 `agents.defaults.model`，无需手动写 `models.providers`。
- **MCP 是工具扩展的标准路径**：通过 stdio、SSE（旧兼容）或 Streamable HTTP 接入外部 MCP 服务器，与 OpenClaw 内置工具并行存在，由模型推理阶段统一调度。
- **多智能体协作有两种架构路径**：基于 `agentId`、`accountId`、`bindings` 的确定性路由适合业务域分工，基于 `sessions_spawn` 的任务委托适合专家协作；两者可组合使用。
- **Agent SDK 与 OpenClaw 互补**：Agent SDK 侧重编排逻辑开发，OpenClaw 侧重运行平台管控（渠道接入、安全审批、会话管理），生产系统中可将 Agent SDK 应用作为 OpenClaw 的 Agent 或 MCP 服务器接入。
- **多生态混合是生产常态**：OpenAI 通过兼容接口接入，Ollama 本地模型适合隐私优先或离线兜底场景；不同生态可按任务复杂度和成本要求灵活组合。

### 下一步

附录提供术语表、配置模板、故障排查检查单和命令速查手册，供日常开发与运维快速查阅。

---

> **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
