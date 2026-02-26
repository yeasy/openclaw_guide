## 11.5 本章小结

第十一章把可靠性与安全落到“可配置、可验证、可追溯”的工程机制：多密钥与认证选择让故障切换可审计，回退与冷却让抖动窗口可止血，工具策略与沙箱让高风险能力有确定性边界，诊断与审计让每次放行/拒绝都能复盘。

### 11.5.1 关键结论

- 多密钥治理要显式：密钥用环境注入、选择用明确标识，轮换要有灰度与回滚点。
- 回退链路要可解释：按错误类型分流，记录触发原因、命中规则与回退目标，避免“无声切换”。
- 冷却用于止血：用冷却窗口抑制重试放大，恢复应依赖探针而不是立即放量。
- 防护栏要三层联动：工具策略决定能不能做，沙箱决定在哪里做，审计决定做了什么且能否追溯。

### 11.5.2 读者自检

- [ ] 是否能在密钥失效、限流、超时三类故障下解释系统采取的动作与证据链？
- [ ] 是否能通过故障注入触发回退，并在日志中对账命中规则与冷却窗口？
- [ ] 高风险工具是否默认收敛，仅在受控入口/受控智能体中显式放开，并可快速回滚？

### 11.5.3 下一章预告

[第十二章](../12_extension_engineering/README.md)进入插件扩展与生产落地：如何把扩展能力纳入策略边界、做成可测试可回放的工程完整流程，并形成可上线、可回滚的落地清单。

### 11.5.4 本章参考文献汇总

- 配置 models：https://docs.openclaw.ai/gateway/configuration#models
- Multi-agent sandbox tools：https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
- Models 命令：https://docs.openclaw.ai/cli/models
- Model Failover：https://docs.openclaw.ai/concepts/model-failover
- Security：https://docs.openclaw.ai/gateway/security
- Tools：https://docs.openclaw.ai/tools
