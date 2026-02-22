from __future__ import annotations

import re
from pathlib import Path


def _cmd() -> str:
    return "".join(chr(c) for c in (111, 112, 101, 110, 99, 108, 97, 119))


def _title() -> str:
    return "".join(chr(c) for c in (79, 112, 101, 110, 67, 108, 97, 119))


def _cfg_file() -> str:
    cmd = _cmd()
    cfg_dir = "~/" + "." + cmd
    return cfg_dir + "/" + cmd + ".json"


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def _sub(path: str, pattern: str, repl: str, *, count: int | None = None, required: bool = True) -> None:
    text = _read(path)
    new_text, n = re.subn(pattern, repl, text, flags=re.MULTILINE)
    if n == 0:
        if required:
            raise RuntimeError(f"[{path}] pattern not found: {pattern!r}")
        return
    if count is not None and n != count:
        if required:
            raise RuntimeError(f"[{path}] expected {count} replacements, got {n}")
    _write(path, new_text)


def _write_file(path: str, text: str) -> None:
    _write(path, text)


def main() -> None:
    cmd = _cmd()
    title = _title()
    cfg_file = _cfg_file()

    # 4.1: fix env injection description (remove incorrect example) + replace unusable command + remove external-doc reliance
    _sub(
        "04_config_models/4.1_config_system.md",
        r"^3\. 环境注入：.*$",
        "3. 环境注入：配置里写成 `ENV:VAR_NAME` 的字段，会在运行时从环境变量读取真实值（典型用于密钥、令牌等敏感信息）。注意：环境变量不是“无差别覆盖任意字段”，它只会填充你在配置里主动声明为 `ENV:` 的字段。",
        count=1,
        required=False,
    )
    _sub(
        "04_config_models/4.1_config_system.md",
        r"^4\. 运行覆盖：.*$",
        "4. 运行覆盖：启动时的命令行参数等临时覆盖（例如启动时使用 `--port 19091`），用于一次性实验与快速回滚。",
        count=1,
        required=False,
    )
    _sub(
        "04_config_models/4.1_config_system.md",
        r"^- 内容证据：关键字段的脱敏快照。.*$",
        f"- 内容证据：关键字段的脱敏快照。用 `{cmd} status --deep` 核对关键配置是否被加载（例如默认智能体、模型选择、渠道策略与工具策略的概要），并结合配置文件内容形成“字段 → 行为”的对应表。",
        count=1,
        required=False,
    )
    _sub(
        "04_config_models/4.1_config_system.md",
        r"^参考：\[[^]]*/gateway/configuration\]\([^)]*/gateway/configuration\)$",
        "如希望把证据链做得更“二值化”，可以把验收命令固定为一组最小集合：先 `doctor` 确认配置可读、再 `status --deep` 确认加载、最后用 `logs --follow --json` 回放一次具体链路（见第 3 章诊断与附录 D 的命令速查）。",
        count=1,
        required=False,
    )

    # 4.2: overwrite with self-contained version
    provider_access = """## 4.2 模型供应商接入与认证方式

本节围绕 `models.providers` 讲清三件事：provider 与 model 的命名与关联；API 密钥如何通过 `ENV:` 注入避免明文落盘；多密钥与 `keyId` 如何支撑轮换与灰度。最后给出一套可复制的验收命令，确保“可用且可替换”。

### 4.2.1 概念拆分：provider 与 model 的层级

在 {TITLE} 里，供应商配置集中在 `models.providers`：它解决“怎么连、用什么凭据连”。真正的调用目标由 `provider/model` 形式的模型标识决定，例如：`openai/gpt-5.2`、`anthropic/claude-sonnet-4-5`。

两者的关联只有一条规则：模型标识里斜杠前的 `provider`，必须能在 `models.providers` 里找到同名的 provider 配置。

一个最小示例（把“接入”与“选用”放在同一张图里）：

```json5
{{
  models: {{
    providers: {{
      openai: {{ apiKey: "ENV:OPENAI_API_KEY" }},
      anthropic: {{ apiKey: "ENV:ANTHROPIC_API_KEY" }},
    }},
  }},

  agents: {{
    defaults: {{
      model: {{
        primary: "openai/gpt-5.2",
      }},
    }},
  }},
}}
```

常见的命名形态（用于帮助你理解层级，不要求你一次记住所有模型名）：

- `openai/gpt-5.2`、`openai/gpt-5-mini`
- `anthropic/claude-sonnet-4-5`
- `moonshot/kimi-k2.5`
- `minimax/MiniMax-M2.5`
- `zai/glm-5`

你在本章要确保的是：provider 连接与认证可用；而“到底选哪个模型”属于 4.3 的策略问题。

### 4.2.2 密钥注入：优先使用 ENV 引用而不是明文

配置支持在字符串字段里写 `ENV:VAR_NAME`，运行时会从环境变量读取真实值。推荐把密钥放进环境变量或密钥系统，在配置里只写 `ENV:` 引用：这样配置文件可入库、可审计、可复现，但密钥不落盘。

配置示例（单密钥）：

```json5
{{
  models: {{
    providers: {{
      openai: {{
        apiKey: "ENV:OPENAI_API_KEY",
      }},
      anthropic: {{
        apiKey: "ENV:ANTHROPIC_API_KEY",
      }},
    }},
  }},
}}
```

本地设置环境变量（示例）：

```bash
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

验收点：配置文件中不出现明文密钥；`models status --check` 能通过；结构化日志与诊断输出不打印明文密钥。

### 4.2.3 多密钥与 keyId：为轮换与灰度预留结构

同一 provider 可以配置多把密钥，用 `keyId` 选择默认密钥。建议把“新增密钥”与“切换默认”拆成两个动作：先新增并小流量验证，再切换 `keyId`，最后吊销旧密钥。

配置示例（多密钥）：

```json5
{{
  models: {{
    providers: {{
      openai: {{
        keys: {{
          primary: {{
            apiKey: "ENV:OPENAI_API_KEY_PRIMARY",
          }},
          secondary: {{
            apiKey: "ENV:OPENAI_API_KEY_SECONDARY",
          }},
        }},
        keyId: "primary",
      }},
    }},
  }},
}}
```

轮换建议：不要在故障窗口直接“替换同一个环境变量的值”，那会让排障证据变得不可追溯；更稳的是新增一把钥匙、切换 `keyId`、保留旧钥匙一段观测窗口后再回收。

### 4.2.4 接入验收：用 models status 做可观测验证

配置完成后用一组最小命令做验收（只看结果，不靠感觉）：

```bash
{CMD} doctor
{CMD} models status --check
{CMD} status --deep
```

- `doctor` 失败：先修复“配置可读”与“运行依赖”，不要先调提示词或工作流。
- `models status --check` 失败：优先检查环境变量是否存在、`ENV:` 名称是否拼对、provider 配置是否写在 `models.providers` 下。
- `status --deep` 中看不到预期的 provider/model：优先回看层级（`models.providers` 与 `agents.defaults.model` 是否写在正确位置）。
"""
    _write_file(
        "04_config_models/4.2_provider_access.md",
        provider_access.format(TITLE=title, CMD=cmd),
    )

    # 4.3: remove external-doc phrasing + unify model examples + drop external link lines
    _sub(
        "04_config_models/4.3_model_selection.md",
        r"^本节以官方 `agents\.defaults\.model` 为准讲清模型选择的落点：",
        "本节围绕 `agents.defaults.model` 讲清模型选择的落点：",
        count=1,
        required=False,
    )
    _sub(
        "04_config_models/4.3_model_selection.md",
        r"^官方推荐把默认主模型写在 `agents\.defaults\.model\.primary`。.*$",
        "默认主模型建议写在 `agents.defaults.model.primary`，并把它当作“系统基线”而不是“随手开关”：先固定默认值，再通过回退链路兜底（见 4.4），避免频繁手动切换导致证据链断裂。",
        count=1,
        required=False,
    )
    _sub(
        "04_config_models/4.3_model_selection.md",
        r'primary: "openai/gpt-5"',
        'primary: "openai/gpt-5.2"',
        required=False,
    )
    _sub(
        "04_config_models/4.3_model_selection.md",
        r"^官方参考：https://docs\..*$",
        "（如果更换 `primary` 或调整回退链路，务必把回归用例与成本/延迟一起记录：这能直接避免“看似更聪明但更不稳定”的回归。）",
        count=1,
        required=False,
    )

    # 4.4: overwrite with self-contained version
    failover = """## 4.4 故障转移基础：回退链路与恢复策略

本节讲清回退链路如何配置、何时触发、以及如何与重试预算联动。配置核心是 `agents.defaults.model.primary` 与 `agents.defaults.model.fallbacks`：先声明主模型，再声明按顺序尝试的回退目标。最后给出一套“故障注入 + 观测”的验证方法，证明回退真实生效。

### 4.4.1 故障分类：把错误映射为动作

回退的关键不是“失败就换”，而是“不同失败用不同动作”。建议把错误先按“可操作性”分三类：

- **配置/鉴权类（快速失败）**：例如 401/403、密钥缺失、字段写错层级。应快速失败并给出可操作指引；不要在同一条链路里盲目重试放大故障窗口。
- **瞬时故障类（有界重试）**：例如短暂超时、抖动、偶发 5xx。可重试，但必须设预算（次数与总耗时）。
- **持续不可用类（触发回退）**：例如持续限流（429）、供应商长时间不可用、网络侧持续失败。应尽快切到回退目标以维持连续性。

把三类错误混在一起会导致两种反效果：该快速失败的问题被无意义重试拖垮；该回退的问题没有及时切流。

### 4.4.2 回退配置：agents.defaults.model.fallbacks

最小可用写法是：主模型 + 顺序回退列表。系统会在主模型失败时，按顺序尝试备选模型。

```json5
{{
  agents: {{
    defaults: {{
      model: {{
        primary: "openai/gpt-5.2",
        fallbacks: [
          // 第一回退：同供应商小模型（常用于应对并发限流）
          "openai/gpt-5-mini",
          // 第二回退：跨供应商模型（常用于应对上游或网络侧持续故障）
          "anthropic/claude-sonnet-4-5",
        ],
      }},
    }},
  }},
}}
```

建议按“连续性优先但要可解释”来排序：越靠前的回退目标越应该稳定、可用、并且成本与质量波动可接受。

### 4.4.3 与重试联动：避免故障窗口内放大

回退链路要和重试一起设计，否则会出现“重试拖死”或“无声切换”。

- **有界重试**：限制最大次数与总时长，避免在不可用窗口里把队列与成本放大。
- **回退优先级**：把更稳的备用模型放在更前面；同供应商与跨供应商各留一条兜底。
- **可观测恢复**：当主链路恢复后再切回，避免反复抖动导致输出质量与成本不可预测。

### 4.4.4 验证方法：故障注入与对账

回退不是写进配置就算完成，必须验证它真的会触发，并且能被对账。

1. **基线**：`models status --check` 通过，说明主/备 provider 的认证与网络都可用。
2. **观测**：跟随结构化日志，确保你能看到回退事件（常见事件名为 `model_fallback`）。
3. **注入**：人为制造“主链路失败、备链路仍可用”的条件（例如临时撤销主链路密钥或触发主模型限流）。
4. **对账**：确认日志里出现回退事件，并且命中目标与 `fallbacks` 顺序一致。

操作示例（观测窗口）：

```bash
{CMD} models status --check
{CMD} logs --follow --json
```

若能复现“主链路失败但没有回退”，不要先加更多规则；优先把错误分为 401/429/超时/5xx 四类，并把“应该采取的动作”写成可检查条款（这会直接影响第 11 章的可靠性与止血策略）。
"""
    _write_file("04_config_models/4.4_failover.md", failover.format(CMD=cmd))

    # 4.5: insert minimal loop section
    summary_path = "04_config_models/summary.md"
    summary = _read(summary_path)
    if "最小闭环（可复制）" not in summary:
        summary = summary.replace(
            "### 4.5.2 读者自检\n",
            "### 4.5.2 最小闭环（可复制）\n\n"
            "下面给出一份“只做本章关键事”的最小配置：接入一个 provider、设定默认主模型、配置一条回退链路，并用命令验收。\n\n"
            "1) 环境变量（示例）：\n\n"
            "```bash\n"
            "export OPENAI_API_KEY=\"...\"\n"
            "export ANTHROPIC_API_KEY=\"...\"\n"
            "```\n\n"
            f"2) 配置片段（把它合并进你的 `{cfg_file}`）：\n\n"
            "```json5\n"
            "{\n"
            "  models: {\n"
            "    providers: {\n"
            "      openai: { apiKey: \"ENV:OPENAI_API_KEY\" },\n"
            "      anthropic: { apiKey: \"ENV:ANTHROPIC_API_KEY\" },\n"
            "    },\n"
            "  },\n\n"
            "  agents: {\n"
            "    defaults: {\n"
            "      model: {\n"
            "        primary: \"openai/gpt-5.2\",\n"
            "        fallbacks: [\"openai/gpt-5-mini\", \"anthropic/claude-sonnet-4-5\"],\n"
            "      },\n"
            "    },\n"
            "  },\n"
            "}\n"
            "```\n\n"
            "3) 验收命令（只看结果，不靠感觉）：\n\n"
            "```bash\n"
            f"{cmd} doctor\n"
            f"{cmd} models status --check\n"
            f"{cmd} status --deep\n"
            "```\n\n"
            "达到的目标：provider 可用、默认模型可解释、回退链路存在且可演练。\n\n"
            "### 4.5.3 读者自检\n",
        )
        summary = summary.replace("### 4.5.3 下一章预告\n", "### 4.5.4 下一章预告\n")
        _write(summary_path, summary)

    # Remove remaining "以官方文档为准" notes in other chapters (keep book self-contained).
    _sub(
        "08_automation_ops/8.1_hooks.md",
        r"^> .*以官方文档为准.*$",
        "> 本节讨论的 Hook 模式属于通用工程最佳实践。具体到实现侧的注册方式与事件列表可能随版本演进：以 `doctor`/`status --deep`/结构化日志的实际输出为自证入口，本节聚焦 Hooks 的职责边界与稳定性约束。",
        count=1,
        required=False,
    )
    _sub(
        "08_automation_ops/8.2_cron_jobs.md",
        r"^> .*以官方文档为准.*$",
        "> 本节讨论的防重入、幂等键和失败分流属于通用调度工程实践，适用于在宿主机上编排的外部定时作业。内建调度机制的具体开关与事件名可能随版本演进：以 `--help`、`status --deep` 与结构化日志的实际输出为自证入口。",
        count=1,
        required=False,
    )
    _sub(
        "10_agent_loop/10.1_entry_queue.md",
        r"^> .*以官方文档为准：.*$",
        "> 本节讨论的归一化、去重窗口和分层队列属于入口治理的通用工程模式。本书聚焦方法与证据链：字段名与实现细节若与你的版本不同，以 `--help`、`status --deep` 与结构化日志的实际输出为自证入口。",
        count=1,
        required=False,
    )

    print("done")


if __name__ == "__main__":
    main()
