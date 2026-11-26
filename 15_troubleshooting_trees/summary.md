## 15.3 本章小结

本章以决策树的形式，提供了覆盖启动失败、消息接收、模型调用、工具执行、会话内存和性能退化六大类故障的系统化排查流程。

### 要点回顾

- **分支诊断**：每棵决策树都按症状分支逐步缩小范围，关键分支给出取证命令，最终导向具体解决方案。
- **`openclaw doctor` 优先**：`doctor` 是配置校验、迁移与修复入口；`--deep` 主要增加对额外 Gateway 安装和系统服务的扫描，不应把它理解成“所有问题的一键深度探测”。
- **高并发场景**：并发限制、连接池耗尽、队列堆积和级联故障需要专门的诊断路径，重点关注限流配置与熔断机制。
- **预防重于修复**：建议每周运行 `openclaw doctor` 与 `openclaw status --all`，每天监控延迟和错误率，每月进行日志与权限审计；`doctor --deep` / `gateway status --deep` 更适合怀疑重复服务或系统级残留时使用。

### 下一步

[第十六章：与主流 AI 生态集成](../16_claude_ecosystem/README.md)介绍 Claude、OpenAI 与本地模型的接入方式，以及多智能体协作，附录提供命令速查手册和故障排查检查单。

---

> **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
