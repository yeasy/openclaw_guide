[中文文档](README.md)

<div align="center">

# OpenClaw: Beginner to Expert

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/yeasy/openclaw_guide?style=social)](https://github.com/yeasy/openclaw_guide)
[![Online Reading](https://img.shields.io/badge/Read_Online-GitBook-brightgreen)](https://yeasy.gitbook.io/openclaw_guide)

> **[OpenClaw](https://github.com/openclaw/openclaw) is an open-source, self-driven AI agent**, created by Peter Steinberger. This book provides a comprehensive guide from getting started to production deployment, with deep dives into the underlying mechanisms and implementation principles.

<img src="cover.jpg" alt="OpenClaw Guide Cover" width="300" />

</div>

## Highlights

- **Hands-on**: Build a minimal working loop from scratch, with ready-to-use configuration templates
- **Deep Dives**: Detailed analysis of Gateway, Agent Loop, tool system, sessions and memory
- **Production-Ready**: Focus on reliability, security hardening, monitoring and troubleshooting

## Target Audience & Prerequisites

- **Target Audience**: Individual users interested in AI agents, AI application developers, LLM engineers, system architects, etc.
- **Prerequisites**: Basic command-line experience is sufficient; programming knowledge is helpful but not required. For those unfamiliar with LLMs and AI agents, see [AI Beginner Guide](https://github.com/yeasy/ai_beginner_guide) and [Agentic AI Guide](https://github.com/yeasy/agentic_ai_guide).

## Book Structure

| Part | Chapters | Overview |
|------|----------|----------|
| Part 1: Getting Started | Ch 1–4 | Overview, setup, first conversation, configuration & model access |
| Part 2: Advanced Usage | Ch 5–8 | Tools & skills, context memory, multi-agent collaboration, automation & ops |
| Part 3: Internals & Engineering | Ch 9–12 | Gateway protocol, Agent Loop internals, reliability, plugin extensions |
| Part 4: Practice & Optimization | Ch 13–16 | Case studies, performance & cost optimization, troubleshooting, AI ecosystem integration |
| Appendix | — | Glossary, config templates, troubleshooting checklist, API reference, command cheatsheet, version mapping, further reading |

## How to Read

### Online

- [GitBook Online](https://yeasy.gitbook.io/openclaw_guide/)
- [Start from Chapter 1](01_overview/README.md)

### Local Preview

This repository uses Honkit for building. For local preview:

```bash
npm install
npm run serve
```

Other Markdown previewers can be used as auxiliary tools, but they are not the standard build chain for this repository.

## 5-Minute Quick Start

New to OpenClaw? Just three steps:

1. **Install** (1 min): `curl -fsSL https://openclaw.ai/install.sh | bash`
2. **Initialize** (2 min): `openclaw` → follow the wizard to configure your model API key
3. **Chat** (2 min): Type "hello" in WebChat, receive an AI response — you're done! 🎉

See [Chapter 2: Setup](02_setup/README.md) and [Chapter 3: First Conversation](03_minimal_loop/README.md).

## Learning Paths

Different readers can choose their path:

| Role | Core Chapters | Est. Time | What You'll Achieve |
|------|--------------|-----------|-------------------|
| 🎮 Individual User | 1→2→3→5 | 2-3 hours | Build a personal WhatsApp/Telegram AI assistant |
| 💻 App Developer | 1-7→12 | 8-10 hours | Develop custom tools, skills and multi-agent systems |
| 🔧 Ops Engineer | 2→3→8→11→14→15 | 6-8 hours | Production deployment, security hardening & troubleshooting |
| 🏗️ Architect | 1→9→10→12→16 | 6-8 hours | Understand internals, design enterprise-grade agent architecture |

## Related Books

This book is part of an AI technology series:

| Book | Relationship |
|------|-------------|
| [AI Beginner Guide](https://github.com/yeasy/ai_beginner_guide) | Zero-to-one AI introduction |
| [Prompt Engineering Guide](https://github.com/yeasy/prompt_engineering_guide) | Agent prompt design fundamentals |
| [Context Engineering Guide](https://github.com/yeasy/context_engineering_guide) | Context management & memory architecture |
| [Claude Guide](https://github.com/yeasy/claude_guide) | Claude MCP protocol, tools & Agentic Coding |
| [Agentic AI Guide](https://github.com/yeasy/agentic_ai_guide) | General agent architecture & multi-agent patterns |
| [AI Security Guide](https://github.com/yeasy/ai_security_guide) | Agent security design & attack/defense practices |
| [LLM Internals](https://github.com/yeasy/llm_internals) | Deep dive into LLM architecture |

## Contributing

Welcome to submit [Issues](https://github.com/yeasy/openclaw_guide/issues) or [PRs](https://github.com/yeasy/openclaw_guide/pulls). Especially welcome: typo fixes, broken link repairs, case study additions, and reusable templates.

## License

This book is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
