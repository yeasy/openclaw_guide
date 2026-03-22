## 1.7 本章小结

本章梳理了 OpenClaw 的系统定位、架构全景与核心对象。

### 要点回顾

- 智能体的核心价值在于端到端的任务闭环，而非单轮对话的表面效果。
- OpenClaw 的架构主干由 Gateway 控制平面与 Agent Runtime 执行内核组成；Channels、Tools、Memory 是可独立替换的能力层。
- Gateway、Agent、Node、Tool、Session 五大对象贯穿全书，决定了配置、排障与扩展的切入点。
- OpenClaw 的核心竞争力在于自托管、多渠道接入与本地工具执行三位一体，但不适合强一致性写入或毫秒级实时控制场景。
- Token 成本是容易被低估的开销——只在需要自然语言理解、模糊决策或多步推理的环节使用智能体，其余部分用确定性代码实现。
- 部署前需建立对安全风险（Prompt Injection、权限错配）、模型幻觉风险和服务可用性风险的清醒认识。

### 读者自检

阅读完本章后，尝试回答以下问题：

- 能否用一句话分别定义 Gateway、Agent、Tool、Session，并说明它们各自负责什么？（可参考[附录 A 术语表](../appendix/glossary.md)校对自己的理解）
- 遇到“工具未触发”或“结果回注缺失”类问题时，能否将故障定位到五大对象中的某一个？
- 当前学习目标属于“可用 → 可控 → 可扩展”的哪个阶段？对应的验收标准是否清晰？

### 下一章预告

[第二章](../02_setup/README.md)将进入可复现的工程起点：系统前置检查、安装方式选择、初始化向导与首次运行验收。

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/openclaw_guide/issues) 或 [PR](https://github.com/yeasy/openclaw_guide/pulls)。
