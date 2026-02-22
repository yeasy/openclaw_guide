## 4.5 本章小结

第四章把“模型能调用”升级为“模型可控”。核心不是换更强模型，而是把配置、认证、选择与故障转移做成可解释的系统能力。

### 4.5.1 关键结论

- 配置决定行为：先分清作用域，再谈优先级与生效证据。
- 供应商接入要可替换：密钥注入、环境隔离与轮换是底线。
- 模型选择要工程化：质量/成本/延迟/可靠性四维，依赖固定用例库回归。
- 故障转移要可验证：重试、轮换、回退、冷却必须能在演练中触发并被解释。

### 4.5.2 最小闭环（可复制）

下面给出一份“只做本章关键事”的最小配置：接入一个 provider、设定默认主模型、配置一条回退链路，并用命令验收。

1) 环境变量（示例）：

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

2) 配置片段（把它合并进你的 `~/.openclaw/openclaw.json`）：

```json5
{
  models: {
    providers: {
      openai: { apiKey: "${OPENAI_API_KEY}" },
      anthropic: { apiKey: "${ANTHROPIC_API_KEY}" },
    },
  },

  agents: {
    defaults: {
      model: {
        primary: "openai/gpt-5.2",
        fallbacks: ["openai/gpt-5-mini", "anthropic/claude-sonnet-4-5"],
      },
    },
  },
}
```

3) 验收命令（只看结果，不靠感觉）：

```bash
openclaw doctor
openclaw models status --check
openclaw status --deep
```

达到的目标：provider 可用、默认模型可解释、回退链路存在且可演练。

### 4.5.3 读者自检

- 能否说明“某个配置字段最终生效值”的证据链（配置路径、体检、日志）？
- 是否具备至少一主一备两条模型链路，并完成最小验收？
- 当出现 401/429/超时/5xx 时，系统分别应该采取什么动作？

### 4.5.4 下一章预告

第五章进入工具系统、技能与插件：把“会回答”升级为“会行动”，并把行动能力收敛在最小权限与可审计边界内。
