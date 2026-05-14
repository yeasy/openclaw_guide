## 附录B：配置模板与样例

本附录提供与官方配置结构对齐的 JSON5 示例，用于快速搭建最小可用系统，并给出可逐步演进到生产的配置组织方式。字段细节可能随版本演进，建议在变更后用 `doctor`、`status` 做一次验证。

### B.1 配置文件位置与格式

OpenClaw Gateway 的主配置文件默认路径为 `~/.openclaw/openclaw.json`。当前更准确的表述是：配置文件按 JSON5 解析；本书中的示例使用带注释的 JSON5 风格展示结构，便于阅读与维护。

建议把配置治理拆成两层。

- 结构层：渠道策略、会话与记忆、工具治理、诊断配置等稳定结构。
- 机密层：模型供应商密钥、渠道令牌等敏感字段，通过环境变量或密钥系统注入。

### B.2 最小可用配置（本地模式 + Web 验证）

该示例用于本地起步：打开本地模式，启用诊断落盘，并保留默认智能体工作区。启动后用 `health/status` 验证，再用 Dashboard 进入 Control UI Chat 做最小交互。

> [!WARNING]
> OpenClaw 对配置会有严格的 Schema 校验。配置未知键会导致 Gateway 拒绝启动。

```json5
{
  gateway: {
    mode: "local",
  },

  logging: {
    file: "/tmp/openclaw/openclaw.log",
    level: "info",
    consoleLevel: "info",
    consoleStyle: "pretty",
    // 注意：redaction 会尽力作用于控制台、文件日志、OTLP 与 transcript，但不承诺完整脱敏
    redactSensitive: "tools",
  },

  diagnostics: {
    enabled: true,
    dumpOnCrash: true,
  },

  agents: {
    defaults: {
      workspace: "~/openclaw-workspace",
    },
  },
}
```

操作验证命令：

```bash
openclaw health --json
openclaw status --deep
openclaw dashboard
```

### B.3 WhatsApp 安全起步模板（配对 + 白名单 + 群聊门控）

该示例把触发面收敛到可控范围。

- 私聊：默认配对，陌生私聊必须审批。
- 白名单：只允许明确号码触发。
- 群聊：默认要求提及，并建议配合群组允许列表。

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+15555550123"],

      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],

      groups: {
        "120363000000000000@g.us": { requireMention: true },
      },
    },
  },

  messages: {
    groupChat: {
      mentionPatterns: ["@openclaw"],
    },
  },
}
```

渠道登录与配对审批参考：

- WhatsApp 渠道：https://docs.openclaw.ai/channels/whatsapp
- pairing 命令：https://docs.openclaw.ai/cli/pairing

### B.4 Telegram 最小模板（单账号）

Telegram 以机器人 token 为核心，适合快速验证。该示例展示最小结构与建议的访问控制。

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "${TELEGRAM_BOT_TOKEN}",

      dmPolicy: "allowlist",
      allowFrom: ["tg:123456789"],

      groupPolicy: "disabled",
    },
  },
}
```

Telegram 渠道参考：[Telegram](https://docs.openclaw.ai/channels/telegram)。

### B.5 工具治理模板

工具治理的官方配置以 `tools.profile` 作为基础模板，并包含 `tools.allow` 与 `tools.deny`。默认策略是允许该 profile 下的全部工具；显式 deny 会覆盖 allow；具体渠道还可按群组、房间或 peer 维度做分层治理。参考：[Tools](https://docs.openclaw.ai/tools) 与 [Group tool restrictions](https://docs.openclaw.ai/channels/groups#groupchannel-tool-restrictions-optional)。

```json5
{
  tools: {
    profile: 'coding',
    deny: ['group:runtime'],
  },
  channels: {
    whatsapp: {
      groups: {
        '*': {
          tools: { deny: ['group:runtime', 'write', 'edit', 'apply_patch'] },
        },
      },
    },
    telegram: {
      groups: {
        '*': {
          tools: { deny: ['group:runtime'] },
          toolsBySender: {
            'id:123456789': { alsoAllow: ['write'] },
          },
        },
      },
    },
  },
}
```

### B.6 持久化与记忆模板

持久化与记忆通常分为两部分：会话状态与长期记忆。官方文档对会话与记忆的文件布局、索引方式与裁剪策略有明确描述，建议先通读再落地配置：[会话](https://docs.openclaw.ai/concepts/session)、[记忆](https://docs.openclaw.ai/concepts/memory)、[上下文裁剪](https://docs.openclaw.ai/concepts/session-pruning)、[压缩](https://docs.openclaw.ai/concepts/compaction)。

下面示例展示了常见的“会话与压缩”配置骨架。重点是把会话行为与压缩策略显式化，便于验收与排障。

```json5
{
  session: {
    // 会话的重置、作用域与清理策略
  },
  agents: {
    defaults: {
      // 记忆与上下文压缩的核心开关与策略
      memorySearch: {
        provider: "local"
      },
      contextPruning: {
        mode: "cache-ttl"
      },
      compaction: {
        enabled: true,
        memoryFlush: {
          // 默认启用；需要关闭时才设置 enabled: false
        }
      }
    }
  }
}
```

验收建议以“可观测”为前提：优先通过 `status --deep` 与日志确认会话与记忆相关配置是否被加载，避免只靠主观对话观察。

```bash
openclaw status --deep
openclaw logs --limit 500 --json
```

### B.7 技能文件模板

技能体系用于固化流程方法。当前更贴近实际使用的组织方式是把工作区技能放在 `<workspace>/skills/<skill-name>/SKILL.md`；若通过 `openclaw skills install` 安装，默认也会写入当前工作区的 `skills/` 目录。技能的格式与加载方式见官方说明：[技能机制](https://docs.openclaw.ai/tools/skills)、[技能命令](https://docs.openclaw.ai/cli/skills)。

下面给出一个可直接复用的 `SKILL.md` 模板。

```markdown
---
name: channel-troubleshooting
description: 渠道不回消息、配对失败、群聊不触发时的排障流程
---

# 渠道排障

## 适用场景

渠道不回消息、配对失败、群聊不触发。

## 步骤

1. 运行 `openclaw doctor`。
2. 运行 `openclaw channels capabilities` 或 `openclaw channels status --probe`。
3. 根据日志中的 `traceId` 回放定位。

## 输出要求

输出必须包含：命令、预期输出、异常分支与下一步。
```

> 技能是方法与步骤，不是运行时权限边界；高风险能力仍应由工具策略与沙箱控制。

### B.8 使用说明与验收建议

配置与扩展的验收建议遵循“先自检、再探针、最后做真实交互”的顺序：

- 自检：先确保依赖与配置结构无误。
- 探针：再确认模型与渠道可用。
- 交互：最后再用少量真实消息验证路由、门控与工具策略。

### B.9 历史版本字段迁移映射表

OpenClaw 采取严格的 Schema 校验机制，当您将旧版本配置文件带入新版本系统时，通常会被 Gateway 拒绝启动。遇到此类情况时，您可以通过 `openclaw doctor --repair` 尝试自动修复，或是参考下方给出的常见漂移映射手动修改：

| 老配置形态 / 遗留字段 | 对应的新配置形态 / 最佳实践 | 备注 |
| --- | --- | --- |
| `diagnostics.logPath` | `logging.file` | 日志全系迁移至统一 `logging` 命名空间管理。 |
| `diagnostics.redact` / `maskedEnv` | `logging.redactSensitive` / `redactPatterns` | 旧版中被混在诊断对象中，目前剥离到专注脱敏的日志对象层级。 |
| 配置中直写加密口令 / API Key | 结合 `${VAR}` 的内联环境变量替换或是 `SecretRef` 对象 | 出于审计与泄漏防护的考量，生产环境已不再建议将值硬编码在 JSON 当中。 |
| `ENV:` 开头的魔术字符串 | `${VAR_NAME}` 字符串插值形式 | 原先 `ENV:` 为老版本遗留或口头契约，当前标准执行器将依据 `${}` 来挂接运行时环境。 |
| `routing.allowFrom` / `routing.groupChat.*` | `channels.whatsapp.allowFrom`、`channels.<channel>.groups."*".requireMention`、`messages.groupChat.*` | 迁移不是把整个 `routing.rules` 平移到 `messages.groupChat`：群聊门控属于渠道策略，只有 `historyLimit`、`mentionPatterns` 等通用群聊上下文项进入 `messages.groupChat`。 |
