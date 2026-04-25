## 13.4 本章小结

本章通过两个可直接复现的完整案例（飞书群工作助手、客户支持智能体）和一份垂直行业对照表，演示了 OpenClaw 从最小可运行配置到生产部署的渐进式落地流程。

### 要点回顾

两个案例共享同一套落地方法论：先用最小 `openclaw.json` 跑通核心循环，再逐层叠加能力。具体而言：

- **渐进式配置**：从单智能体 + 单渠道的最小配置出发，每次只增加一个关注点（权限、工具、审计、降级），确保每层变更可独立验证和回滚。
- **工具策略兜底**：利用 `tools.deny`/`tools.allow` 和 `toolsBySender` 实现细粒度权限控制，写操作默认拒绝、按需放开（参见 [11.4 防护栏](../11_reliability_security/11.4_guardrails.md)）。
- **模型分级**：简单任务（FAQ、数据提取）用轻量模型，复杂任务（投诉处理、诊断推理）用高能力模型，在成本与质量之间取得平衡（参见 [第十四章](../14_performance_cost/README.md)）。
- **行业适配**：从通用方案到行业方案的核心差异在于合规审查、人工审核卡点、数据隔离粒度和领域知识库四个维度（参见 [13.3 节](13.3_vertical_industry_cases.md)）。

### 下一步

[第十四章](../14_performance_cost/README.md)将系统讲解性能与成本优化策略，[第十五章](../15_troubleshooting_trees/README.md)提供故障诊断决策树，[第十六章](../16_claude_ecosystem/README.md)介绍与 Claude 生态的深度集成。

---

> **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
