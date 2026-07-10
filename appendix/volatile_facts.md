## 附录J：快变事实核验表

> Last verified: 2026-06-17. 本表用于维护 OpenClaw、模型、API、价格、协议和 workflow 相关高波动事实。

| 类别 | 当前维护口径 | 权威入口 | 编辑要求 |
| --- | --- | --- | --- |
| OpenClaw release | 安装命令、Node 要求、配置字段、CLI 行为以 OpenClaw release 和 docs 为准。 | OpenClaw docs / releases | 任何可复制命令都应能用当前版本复核。 |
| 模型与价格 | OpenAI、Claude、Gemini、本地模型价格与上下文只写 dated snapshot；Claude Fable 5 / Mythos 5 于 2026-06-09 发布，曾于 2026-06-12 起因出口管制暂停访问；截至 2026-07-09，官方模型页已恢复将 Fable 5 列为正常提供（GA）、Mythos 5 为受限可用（以模型页现状为准）。 | [OpenAI Models](https://developers.openai.com/api/docs/models/all/), [Claude Models](https://platform.claude.com/docs/en/about-claude/models/overview), [Fable/Mythos access statement](https://www.anthropic.com/news/fable-mythos-access), [Gemini Models](https://ai.google.dev/gemini-api/docs/models) | 预算模板必须标注假设和核验日期；Claude 侧“最强/旗舰”须区分发布规格、当前可用性、Fable 5（全系）与 Opus 4.8（Opus 档）。 |
| MCP / A2A / ACP | 协议字段、transport、auth、agent-to-agent 能力以规范为准。 | [MCP Spec](https://modelcontextprotocol.io/specification), [A2A Spec](https://github.com/a2aproject/A2A/blob/main/docs/specification.md) | 框架互操作章节必须区分已实现与设计建议。 |
| Release workflow | mdpress、GitHub Actions、release action 版本必须固定并校验。 | mdPress release、GitHub Actions 官方仓库 | 不使用 unpinned latest 构建正式 PDF。 |
| 示例配置 | 真实 schema 与设计骨架要分开维护。 | OpenClaw schema / docs | 不能直接运行的示例必须显式标注。 |
