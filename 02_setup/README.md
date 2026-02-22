# 第二章：环境准备与安装部署

本章旨在指导在本地或服务器环境中部署 OpenClaw。

**本章学习目标**

- 明确并验证运行 OpenClaw 所需的 Node.js 版本、网络连通性及账号密钥前置条件。
- 掌握使用官方脚本和 npm 安装方式的流程，并建立版本治理与回滚意识。
- 深刻理解 `openclaw onboard` 初始化向导的实质输出，掌握 `openclaw.json` 的关键配置项。
- 建立并熟练运用标准的“首跑验证体系”与基础故障排除指南。

**适用范围**

本指南适用于 macOS、Linux 及 Windows（建议使用 WSL2）环境。在生产级部署中，强烈建议采用 Linux 主机搭配 Docker，并辅以反向代理、进程守护程序以及严格的最小权限账号策略。

**章节地图**

- [2.1 系统要求与运行前检查](2.1_requirements.md)
- [2.2 安装 OpenClaw](2.2_installation.md)
- [2.3 初始化向导与首轮配置](2.3_onboarding.md)
- [2.4 守护进程与可用性验收](2.4_gateway_service.md)
- [2.5 本章小结](summary.md)
