## 附录F：版本映射与升级指南

本附录不再把某一代旧字段硬写成“当前配置”，而是给出一套更安全的升级方法：先识别当前 schema 家族，再用 `doctor`、`config validate` 和 `config get/set/unset` 做增量迁移。

> [!WARNING]
> OpenClaw 使用日历版本号（CalVer），字段层级与命名可能随版本演进而变化。本附录仅提供迁移思路与当前 live 审计实例（2026.3.30）的可观察结构，不能替代官方文档与本地 `config schema`。

### F.1 版本号方案

OpenClaw 采用**日历版本号（CalVer）**，格式为 `YYYY.M.D`：

- `YYYY`：发布年份
- `M`：发布月份
- `D`：发布日期

示例：

```text
2025.11.15  →  2026.1.9  →  2026.2.14  →  2026.3.30
```

CalVer 的最大价值是“版本号天然携带时间语义”。做迁移判断时，先确认你当前运行的具体版本，再去看对应文档与 schema 输出。

### F.2 当前 schema 家族速览

在本次 live 审计实例中，最稳定、最值得优先识别的是下面这些 schema 家族。

| 家族 | 当前常见结构 | 说明 |
|------|-------------|------|
| 认证 | `auth.profiles` | 认证档案与 provider 绑定，不再把所有密钥都直接写进单层字段 |
| Agent | `agents.defaults` + `agents.list[]` | “全局默认 + 按 agent 覆盖”是当前更常见的组织方式 |
| 模型 | `agents.defaults.model`（字符串或 `{ primary, fallbacks }`） | 当前 schema 以 `agents.defaults.model` 为主入口；对象形态可显式表达主模型与回退链 |
| 渠道 | `channels.<channel>.dmPolicy` / `groupPolicy` | 私聊与群聊分开治理是当前入口控制的核心 |
| Gateway | `gateway.port` / `gateway.auth.mode` / `gateway.controlUi.allowedOrigins` | 控制面鉴权与来源校验已经是显式结构 |
| Hook | `hooks.internal.entries.*` | 当前 live 实例首先暴露的是内建 hooks，而不是默认目录式 Hook |
| 插件 | `plugins.entries.*` | 用户配置面仍以 `plugins.entries` 为核心；兼容 bundle 只是分发/发现层，不应混同为另一套配置语法 |

把这些家族先识别出来，迁移就不会被某个旧字段名牵着走。

### F.3 从旧结构到当前结构的迁移思路

下面不是“一一精确映射表”，而是当前更安全的迁移方向。

| 历史写法 | 当前更应迁移到 | 迁移原则 |
|---------|---------------|---------|
| 单体 agent 配置 | `agents.defaults` + `agents.list[]` | 先抽公共默认，再做特定 agent 覆盖 |
| `agents.*.model` 单字符串 | `agents.defaults.model.primary` + `agents.defaults.model.fallbacks` | 把模型选择与回退链显式化；如仅需单模型，也可继续使用字符串形态 |
| 渠道单层门控开关 | `dmPolicy` / `groupPolicy` / `groups.*` | 先分清私聊与群聊，再处理提及门控和白名单 |
| 顶层零散安全字段 | `gateway.auth`、`controlUi.allowedOrigins`、`tools` 策略 | 把控制面鉴权、来源校验、执行策略分层 |
| 目录式 Hook 假设 | `hooks.internal.entries.*` | 先看当前版本是否已有内建 Hook 体系，再决定是否需要自定义 Hook |
| 明文 key/file key | `auth.profiles` + `${ENV}` / SecretRef | 优先迁向当前 secrets/环境变量体系 |

### F.4 常见“已过时思路”提示

升级时，最容易踩坑的不是字段拼错，而是**沿用了一整套过时的配置思路**。下面这些情况要特别警惕：

- 把 `agents.default`、`agents.*.models`、`gateway.listeners` 之类写成“当前默认写法”。
- 把 `channels.*.requireMention`、`channels.*.routing[].conditions.requireMention` 这类旧门控路径写成唯一正确答案。
- 把 `auth.type`、`auth.useKeyFile` 之类单层认证字段写成主路径，而忽略 `auth.profiles`。
- 把旧案例里的“可直接粘贴运行”配置直接当成当前版本模板。

更稳妥的做法是：**先用 schema 看家族，再用示例做映射**，而不是反过来。

### F.5 当前可用的迁移命令

当前官方 CLI 中，最实用的是下面几组命令。

#### `openclaw doctor`

`doctor` 负责诊断配置和运行时健康状态，同时会处理当前官方支持的 legacy migration。

```bash
openclaw doctor
openclaw doctor --deep
openclaw doctor --repair
```

> 当前官方 CLI 文档将 `--fix` 视为 `--repair` 的别名；同时，运行时提示和不少诊断输出仍常直接打印 `openclaw doctor --fix`。两者语义等价，实际以本地 `openclaw doctor --help` 为准。

#### `openclaw config`

`config` 用于读取、校验和精确修改配置项。

```bash
openclaw config file
openclaw config validate
openclaw config get gateway.auth.mode
openclaw config set gateway.auth.mode token
openclaw config unset legacy.oldField
```

#### `openclaw secrets`

如果迁移涉及凭据存储，而不是普通字段层级调整，更稳妥的入口是当前官方提供的 `secrets audit / configure / apply / reload` 流程，而不是假定存在某个单独的 `migrate` 子命令：

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets reload
```

### F.6 推荐升级流程

配置升级更适合遵循 **备份 → doctor → validate → 手动补差 → 深度诊断 → 回归测试** 的流程。

#### 快速步骤

```bash
# 1. 备份当前配置目录
cp -r ~/.openclaw ~/.openclaw.backup.$(date +%Y%m%d_%H%M%S)

# 2. 先运行 doctor，处理当前官方已知迁移
openclaw doctor

# 3. 校验配置结构
openclaw config validate

# 4. 精确读取关键配置
openclaw config get gateway.auth.mode
openclaw config get agents.defaults.model.primary

# 5. 按当前 schema 手动补差
openclaw config set gateway.auth.mode token

# 6. 深度诊断
openclaw doctor --deep
```

#### 回滚步骤

```bash
rm -rf ~/.openclaw
mv ~/.openclaw.backup.YYYYMMDD_HHMMSS ~/.openclaw
openclaw gateway restart
```

### F.7 升级时最值得优先复验的项

升级后不要只看“配置校验通过”，还应至少复验以下内容：

1. Control UI 是否仍能正常连接。
2. `gateway.auth.mode` 与 `controlUi.allowedOrigins` 是否符合当前部署方式。
3. 默认 agent 的 `agents.defaults.model.primary` / `agents.defaults.model.fallbacks` 是否仍指向可用模型。
4. `dmPolicy` / `groupPolicy` 是否符合当前入口治理策略。
5. Hook、插件、工具策略是否仍按预期生效。

### F.8 本章小结

版本迁移的关键不是背一张“旧字段 → 新字段”的表，而是先抓住当前 schema 家族：

- 认证看 `auth.profiles`
- Agent 看 `agents.defaults` 与 `agents.list[]`
- 模型看 `agents.defaults.model`
- 渠道看 `dmPolicy / groupPolicy`
- Gateway 看 `auth + controlUi.allowedOrigins`
- Hook 看 `hooks.internal`
- 插件看 `plugins.entries`

先跑 `doctor`，再用 `config validate` 和 `config get/set/unset` 做精确补差，是当前更可靠的升级路径。
