# 第十六章 与主流 AI 生态集成

本章介绍 OpenClaw 与主流 AI 模型生态的集成实践，涵盖 Anthropic Claude、OpenAI、以及以 Ollama 为代表的本地模型。第四章已讲清模型供应商接入和 Fallback 配置的基础用法，本章在此基础上聚焦各生态的特有能力、接入要点，以及在 OpenClaw 中统一管理多生态模型的实践模式。

## 本章内容导读

本章包括以下几个小节：

- **[16.1 Claude 模型接入与 MCP 生态集成](16.1_claude_integration.md)**：Claude 模型家族选型要点、OpenClaw 中的配置方式、MCP 服务器接入与多供应商混合部署。
- **[16.2 多智能体协作与编排模式](16.2_agent_team_integration.md)**：基于 `agentId`、`accountId`、`bindings` 的确定性路由与基于 `sessions_spawn` 的任务委托、串联/并联/路由三种协作模式、工程约束与 Agent SDK 的互补关系。
- **[16.3 OpenAI 与本地模型集成](16.3_other_ecosystems.md)**：OpenAI 模型接入、Ollama 本地模型部署、多生态混合策略。
- **[16.4 本章小结](summary.md)**：关键结论与延伸资源。
