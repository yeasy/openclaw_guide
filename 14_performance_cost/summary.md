## 14.5 本章小结

> **注**：本章定价数据基于各供应商官方 API 定价。AI 模型定价变化频繁，请以各供应商官方定价页面为准：
> - [Anthropic 官方定价](https://platform.claude.com/docs/en/about-claude/pricing)
> - [OpenAI 官方定价](https://openai.com/api/pricing/)

本章从 Token 消耗、推理延迟、用量观测和部署预算四个维度，提供了基于 OpenClaw 内置能力的性能优化与成本控制方案。

### 要点回顾

- **Token 与上下文成本**（14.1）：通过系统提示精简、按 Agent 分配工具定义、`compaction` 与 `contextPruning` 配置实现上下文压缩，配合 `model.primary` / `model.fallbacks` 进行模型分级。
- **延迟与吞吐优化**（14.2）：延迟由网络、队列、模型推理、工具调用四段构成；通过模型回退链、工具并行化和 `openclaw health --json` 渠道监控来定位瓶颈。
- **用量观测与外部预算治理**（14.3）：使用 `/status`、`/usage cost`、`/compact` 等交互命令实时监控 Token 用量，再结合 provider billing limit、外部监控、入口限流或插件实现硬预算与告警。
- **部署预算模板**（14.4）：预算高度依赖 token/request、工具调用占比与基础设施规格；本章模板显示个人通常是几十美元，团队往往很快进入千美元级，企业高并发场景则可能轻易达到数万美元以上。

### 优化检查清单

1. 是否已通过 `/usage cost` 或 `openclaw status --usage` 建立 Token 消耗基线？
2. 系统提示是否已精简到必要最小集？
3. 是否为不同 Agent 配置了差异化的工具集和模型？
4. `compaction` 和 `contextPruning` 策略是否已启用并调优？
5. 模型回退链是否已配置，避免单点故障？
6. 是否有定期的成本审计流程？

### 下一步

第十五章将提供常见故障的诊断决策树，第十六章介绍与 Claude 生态的深度集成。

---

> **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
