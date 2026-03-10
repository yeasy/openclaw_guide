## 16.3 本章小结

本章介绍了 OpenClaw 与 Claude 模型家族、MCP 服务器及第三方工具生态的集成最佳实践。

### 要点回顾

- **多模型策略**：根据任务复杂度选择 Haiku（低成本快速响应）、Sonnet（平衡）或 Opus（高质量推理），配合 Fallback 链提升可用性。
- **MCP 集成**：通过 stdio、HTTP 或 WebSocket 方式接入文件系统、数据库、Git 和自定义 API，实现 Claude 对企业数据的直接访问。
- **Agent Team 协作**：多智能体间通过路由规则与角色分工协同完成复杂任务，子智能体专注特定领域以提升整体效率。
- **安全与合规**：所有 MCP 访问需经过身份验证、权限检查和审计日志，敏感数据需脱敏处理。

### 下一步

附录提供术语表、配置模板、故障排查检查单和命令速查手册，供日常开发与运维快速查阅。

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
