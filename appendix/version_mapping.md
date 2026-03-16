## 附录F：版本映射与配置字段变更记录

本章提供OpenClaw配置字段的演进趋势、废弃字段的替代方案以及升级迁移指南，确保跨版本兼容性与平滑升级。

> **WARNING**: OpenClaw使用日历版本号（CalVer）方案，版本号和配置字段可能随版本更新而变化。本章内容仅作参考，请始终以官方文档和 `openclaw doctor` 诊断工具的输出为准。

### 16.1.1 版本号方案 - CalVer

OpenClaw采用**日历版本号（CalVer）**命名方案，格式为 `YYYY.M.D`：

- **YYYY**：发布年份（如 2026）
- **M**：发布月份（如 1、2、...12，无前导零）
- **D**：发布日期（如 1、2、...31，无前导零）

#### 示例

```text
2025.11.15  →  2026.1.9  →  2026.2.14  →  2026.3.6
  秋季版本      冬季版本      早春版本      当前版本
  Agent基础    多渠道支持    企业级功能    Claude集成增强
  配置体系      Lark/Slack等   K8s支持      成本管理功能
```

#### 优势

- **时间语义**：版本号直接反映发布日期，便于追踪发布周期
- **自然排序**：无需特殊比较逻辑，日期自然排序即为版本顺序
- **快速识别**：用户可根据版本号快速了解功能新旧程度

### 16.1.2 配置结构演进趋势

OpenClaw配置体系按功能模块逐步演进，以下按模块列出主要变更方向：

#### Agent 配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 基础结构 | `agent.name` (单体) | `agents.{agentId}.name` (Map) | 从单Agent改为多Agent支持，便于管理不同角色 |
| 模型配置 | `agents.*.model` (string) | `agents.*.models` (array) | 支持多模型fallback链和优先级权重 |
| 工具绑定 | `agents.*.tools` (Array) | `agents.*.tools` + `agents.*.toolGroups` | 新增工具组概念，支持关联工具的逻辑分组 |
| 上下文管理 | `memory.maxSize` (字符数) | `memory.maxContextTokens` 或 `memory.contextBudget` | 从字符数迭代到Token计数，再到细粒度预算控制 |

#### 渠道配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 认证方式 | `channels.lark.token` (单字段) | `channels.lark.appId` + `appSecret` | 分离认证信息，提升安全性 |
| 限流控制 | `channels.*.rateLimit` (独立) | `gateway.rateLimit` + `profiles.*.rateLimit` | 从渠道级改为网关全局 + Profile单独配置的层级体系 |
| 路由规则 | `channels.*.webhookPath` (平面) | `channels.*.routing[].conditions` | 支持多条件组合的灵活路由 |
| 业务规则 | `channels.*.requireMention` | `channels.*.routing[].conditions.requireMention` | 路由规则化，支持复杂的业务逻辑组合 |

#### 模型配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| Fallback策略 | `failover.strategy` (全局) | `failover.model.strategy` + `failover.tool.strategy` | 支持模型级和工具级分别配置 |
| 多模型支持 | 单一模型 | 模型数组 with weights/priority | 支持权重和优先级，提升可靠性和成本优化 |

#### 网关配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 监听配置 | `gateway.port` (number) | `gateway.listeners` (array) | 支持同时监听多个端口/协议组合 |
| 认证管理 | `security.requireAuth` | `gateway.auth.requirePairing` | 移到Gateway层，概念更准确 |

#### 工具配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 启用控制 | `tools.enabled` (平面) | `tools.{toolId}.enabled` (Map) | 改为按工具ID的Map，便于大规模工具管理 |
| 超时配置 | `tools.*.timeout` (单值) | `tools.*.readTimeout` + `writeTimeout` | 分离读写超时，细粒度控制 |
| 缓存策略 | `tools.*.cache.ttl` (简单TTL) | `tools.*.cache` (object) | 支持LRU、TTL、Size等复杂缓存策略 |
| 权限策略 | `tools.*.policy` (工具级) | `tools.*.policy` + `profiles.*.toolPolicies` | Profile层可覆盖工具级配置，灵活性提升 |

#### 日志与监控演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 日志级别 | `logging.level` (单一) | `logging.levels` (object) | 支持为不同模块设置不同日志级别 |
| 日志轮转 | `logging.singleFile` | `logging.rotation` | 从单文件改为日志轮转策略 |
| Hooks配置 | `hooks.*.script` (string path) | `hooks.*.script` + `hooks.*.inline` | 支持外部脚本文件或内联代码混合 |

#### 安全配置演进

| 演进阶段 | 早期配置 | 当前配置 | 变更说明 |
|--------|--------|--------|--------|
| 密钥管理 | `auth.useKeyFile` | `auth.type: 'environment_variable'` 或 `'secret_manager'` | 从文件转向环境变量或密钥管理服务 |
| 内存压缩 | `memory.compactOnTurns` (简单计数) | `memory.compactionMode` (intelligent/aggressive/balanced) | 从固定阈值改为智能压缩策略 |

### 16.1.3 常见废弃字段与替代方案

以下列出常见的废弃配置字段及其替代方案。具体的版本信息请参考官方变更日志。

```json
{
  "deprecated_fields": [
    {
      "field": "agent.defaultTools",
      "reason": "单体Agent架构被多Agent支持替代",
      "replacement": "agents.{agentId}.tools: ['tool1', 'tool2']",
      "migration_guide": "手动将defaultTools中的工具复制到新的agents结构"
    },
    {
      "field": "auth.useKeyFile",
      "reason": "安全性改进：避免密钥存储在文件中",
      "replacement": "auth.type: 'environment_variable' 或 auth.type: 'secret_manager'",
      "migration_guide": "改用环境变量或密钥管理服务存储认证信息"
    },
    {
      "field": "memory.compactOnTurns",
      "reason": "被更灵活的智能压缩策略替代",
      "replacement": "memory.compactionMode: 'intelligent' | 'aggressive' | 'balanced' | 'conservative'",
      "migration_guide": "选择合适的压缩模式替代固定转数阈值"
    },
    {
      "field": "tools.*.timeout",
      "reason": "读写超时需要分离管理",
      "replacement": "tools.*.readTimeout 和 tools.*.writeTimeout",
      "migration_guide": "将原timeout值分配给read和write两个字段，或根据实际需求设置不同值"
    },
    {
      "field": "channels.*.requireMention",
      "reason": "简单布尔值无法满足复杂业务规则需求",
      "replacement": "channels.*.routing[].conditions.requireMention",
      "migration_guide": "在路由规则层配置，支持多条件组合和优先级"
    },
    {
      "field": "logging.singleFile",
      "reason": "单文件日志难以管理和轮转",
      "replacement": "logging.rotation: { type: 'daily', maxFiles: 30 }",
      "migration_guide": "启用日志轮转策略，自动管理日志文件生命周期"
    },
    {
      "field": "gateway.port",
      "reason": "单端口配置无法满足多协议和多端口需求",
      "replacement": "gateway.listeners: [{ port: 18789, protocol: 'http', host: '0.0.0.0' }]",
      "migration_guide": "将单个port改为listeners数组，支持多端口和协议配置"
    },
    {
      "field": "agents.*.model (string类型)",
      "reason": "单模型配置无法支持fallback和成本优化",
      "replacement": "agents.*.models: [{ model: 'claude-opus-4-6', weight: 0.8, priority: 'primary' }]",
      "migration_guide": "转换为models数组，支持fallback链、权重和优先级"
    },
    {
      "field": "channels.*.rateLimit",
      "reason": "渠道级限流改为网关层面的统一管理",
      "replacement": "gateway.rateLimit (全局) + profiles.*.rateLimit (按profile覆盖)",
      "migration_guide": "将限流配置上移到网关层，支持Profile级的细粒度覆盖"
    }
  ]
}
```text

**处理废弃字段的通用流程：**

1. 使用 `openclaw config validate` 检查配置中的废弃字段
2. 参考上表找到替代方案
3. 使用 `openclaw config migrate` 自动迁移，或手动更新配置
4. 运行 `openclaw doctor` 验证新配置的有效性

### 16.1.4 配置迁移工具

OpenClaw提供两个关键的配置管理命令：

#### openclaw config migrate

自动检测当前配置结构并进行迁移，将过时的字段转换为当前版本的格式。

**基本用法：**

```bash
# 自动迁移到最新格式
openclaw config migrate ~/.openclaw/openclaw.json

# 迁移到指定格式，同时生成备份
openclaw config migrate \
  --input ~/.openclaw/openclaw.json \
  --output ~/.openclaw/openclaw.new.json \
  --backup ~/.openclaw/openclaw.backup.$(date +%s).json

# 查看迁移变更详情
openclaw config migrate \
  --input ~/.openclaw/openclaw.json \
  --dry-run \
  --verbose
```text

**迁移流程：**

1. **检测阶段**：自动识别配置中的过时字段和结构
2. **转换阶段**：应用规则集逐步转换为当前格式
3. **验证阶段**：使用JSON Schema验证转换结果的有效性
4. **备份阶段**：自动备份原配置文件
5. **应用阶段**：将新配置写入目标文件

#### openclaw doctor

诊断配置的健康状态，检测问题并提供修复建议。

**基本用法：**

```bash
# 完整诊断
openclaw doctor

# 诊断并生成修复报告
openclaw doctor --detailed

# 针对特定配置文件诊断
openclaw doctor --config ~/.openclaw/openclaw.json

# 自动修复问题（需谨慎）
openclaw doctor --auto-fix
```text

**诊断项目：**

- 过时字段检测：识别已弃用的配置字段
- 必需字段检查：确保所有必需的配置字段存在
- 类型验证：检查字段类型是否符合预期
- 值范围检查：验证字段值在有效范围内
- 依赖关系验证：确保配置之间的依赖关系满足
- Agent健康检查：验证Agent配置的完整性
- 渠道连接测试：测试各渠道的连接状态
- 权限检查：验证认证配置的合法性

**输出示例：**

```
OpenClaw Configuration Doctor
版本: 2026.3.6
配置文件: ~/.openclaw/openclaw.json

检查项目:
  [✓] 必需字段检查 - 全部通过
  [✓] 字段类型验证 - 全部通过
  [⚠] 过时字段检测 - 发现2个
    - agents.default.model 应改为 agents.default.models (array)
    - gateway.port 应改为 gateway.listeners (array)
  [✓] Agent配置健康 - 2个Agents正常
  [✓] 渠道连接测试 - Lark, Slack 连接正常
  [✗] 权限检查 - 发现问题
    - 错误: channels.slack.token 不能为空

修复建议:
  1. 运行 'openclaw config migrate --auto-fix' 自动修复过时字段
  2. 在 ~/.openclaw/openclaw.json 中补充 channels.slack.token
  3. 运行 'openclaw doctor' 重新诊断
```text

**Doctor与Migrate的协作：**

通常的工作流程为：

```bash
# 1. 首先诊断配置问题
openclaw doctor

# 2. 自动修复过时字段
openclaw config migrate --auto-fix

# 3. 再次诊断确认修复成功
openclaw doctor

# 4. 如果还有问题，根据提示手动修改配置
vi ~/.openclaw/openclaw.json

# 5. 最后验证配置有效性
openclaw config validate ~/.openclaw/openclaw.json
```text

### 16.1.5 向后兼容性说明

OpenClaw使用滚动支持政策，确保用户有充足的时间升级，同时保持代码库的可维护性。

#### 兼容性原则

- **最新版本**：始终支持当前发布的版本
- **次新版本**：支持前一个月份的版本（例如3月发布的版本可读2月的配置）
- **更旧版本**：不再保证完全兼容，但 `openclaw config migrate` 可自动转换

#### 配置兼容性模型

```
当前时间：2026.3.6

支持的配置版本：
  ✓ 2026.3.* 及更新的配置 - 完全支持（原生格式）
  ✓ 2026.2.* 的配置 - 向后兼容（可自动迁移）
  ⚠ 2026.1.* 及更旧的配置 - 需要使用 openclaw config migrate 转换
  ✗ 非常古老的配置 - 可能无法自动转换，需要手动检查
```text

#### 版本跨度支持

```
OpenClaw版本        可读配置版本范围           处理方式
────────────────────────────────────────────────────────
2026.3.6 (当前)     2026.2.* 到最新           原生支持/自动迁移
2026.2.*            2026.1.* 到 2026.2.*      原生/迁移/部分兼容
2026.1.*            仅2026.1.* 及更新         原生支持
```text

#### 处理旧版本配置的步骤

对于来自较旧版本的配置文件，推荐流程：

```bash
# 1. 备份原文件
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.old

# 2. 尝试自动迁移
openclaw config migrate \
  --input ~/.openclaw/openclaw.json.old \
  --output ~/.openclaw/openclaw.json

# 3. 验证迁移结果
openclaw doctor --detailed

# 4. 如果doctor报告问题，手动修正
# 根据doctor的建议进行修改

# 5. 最终验证
openclaw config validate ~/.openclaw/openclaw.json
```text

### 16.1.6 配置升级与迁移步骤

OpenClaw配置升级遵循**备份 → 迁移 → 验证 → 部署**的标准流程。

#### 快速升级流程

```bash
#!/bin/bash
# upgrade_openclaw.sh - 配置升级脚本

set -e

CURRENT_VERSION=$(openclaw version)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONFIG_DIR=~/.openclaw

echo "========================================="
echo "OpenClaw 配置升级"
echo "========================================="
echo "当前版本: $CURRENT_VERSION"
echo "配置目录: $CONFIG_DIR"
echo ""

# 步骤1：完整备份
echo "[1/4] 创建完整备份..."
cp -r "$CONFIG_DIR" "$CONFIG_DIR.backup.$TIMESTAMP"
echo "✓ 备份完成: $CONFIG_DIR.backup.$TIMESTAMP"
echo ""

# 步骤2：自动迁移配置
echo "[2/4] 迁移配置文件..."
if openclaw config migrate "$CONFIG_DIR/openclaw.json" --auto-fix; then
  echo "✓ 配置迁移成功"
else
  echo "✗ 配置迁移失败，已恢复备份"
  rm -rf "$CONFIG_DIR"
  mv "$CONFIG_DIR.backup.$TIMESTAMP" "$CONFIG_DIR"
  exit 1
fi
echo ""

# 步骤3：诊断检查
echo "[3/4] 运行诊断检查..."
if openclaw doctor --config "$CONFIG_DIR/openclaw.json"; then
  echo "✓ 诊断通过"
else
  echo "⚠ 诊断发现问题，请查看上方输出"
  echo "  可手动编辑配置文件进行修正"
fi
echo ""

# 步骤4：总结
echo "[4/4] 升级完成"
echo "========================================="
echo "下一步建议："
echo "  1. 审查迁移的配置: cat $CONFIG_DIR/openclaw.json"
echo "  2. 在非生产环境测试新配置"
echo "  3. 如需回滚，使用备份: cp -r $CONFIG_DIR.backup.$TIMESTAMP $CONFIG_DIR"
echo "========================================="
```text

#### 分步详解

**步骤1：备份当前配置**

```bash
# 创建完整的配置备份
cp -r ~/.openclaw ~/.openclaw.backup.$(date +%Y%m%d)

# 或仅备份配置文件
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
```text

**步骤2：迁移配置**

```bash
# 自动迁移，应用所有必要的转换
openclaw config migrate ~/.openclaw/openclaw.json

# 或查看迁移变更但不应用（dry-run模式）
openclaw config migrate ~/.openclaw/openclaw.json --dry-run --verbose
```text

**步骤3：诊断验证**

```bash
# 完整诊断
openclaw doctor

# 详细诊断，包含修复建议
openclaw doctor --detailed

# 针对特定配置
openclaw doctor --config ~/.openclaw/openclaw.json
```text

**步骤4：处理问题**

如果诊断发现问题：

```bash
# 方案A：自动修复（仅修复明确的问题）
openclaw doctor --auto-fix

# 方案B：手动编辑
vim ~/.openclaw/openclaw.json

# 然后重新验证
openclaw config validate ~/.openclaw/openclaw.json
```text

#### 非生产环境测试

升级前强烈建议在测试环境验证：

```bash
# 1. 在测试环境复制完整的OpenClaw部署
docker run --name openclaw-test \
  -v ~/.openclaw:/root/.openclaw \
  openclaw:latest

# 2. 运行迁移
docker exec openclaw-test openclaw config migrate

# 3. 运行诊断
docker exec openclaw-test openclaw doctor

# 4. 执行功能测试
docker exec openclaw-test openclaw test --config ~/.openclaw/openclaw.json

# 5. 查看日志确认运行状态
docker logs openclaw-test
```text

#### 回滚步骤

如果升级后遇到问题，快速回滚：

```bash
# 恢复备份
rm -rf ~/.openclaw
mv ~/.openclaw.backup.YYYYMMDD ~/.openclaw

# 重启OpenClaw服务
systemctl restart openclaw
# 或
docker restart openclaw-container
```text

#### 常见问题处理

**问题1：迁移后诊断报告过时字段**

```bash
# 查看具体的过时字段
openclaw doctor --detailed

# 参考16.1.3章节的废弃字段对照表手动修正
vim ~/.openclaw/openclaw.json

# 再次诊断
openclaw doctor
```text

**问题2：特定渠道连接失败**

```bash
# 诊断输出会指示具体渠道
openclaw doctor

# 检查该渠道的认证配置
# 例如：channels.lark.appId/appSecret 是否正确设置
# 例如：channels.slack.token 是否为空

# 修复后重新诊断
openclaw doctor
```text

**问题3：Agent配置不完整**

```bash
# 确保每个Agent都有必需的字段：
# - agents.{agentId}.name (string)
# - agents.{agentId}.models (array)
# - agents.{agentId}.tools (array, 可以为空)

# 参考16.1.2中的Agent配置演进部分
vim ~/.openclaw/openclaw.json
```

#### 本章小结

配置升级的核心原则：

1. **总是备份** - 保留升级前的完整快照
2. **逐步迁移** - 使用 `openclaw config migrate` 自动转换
3. **充分验证** - 用 `openclaw doctor` 检查健康状态
4. **测试确认** - 在非生产环境完整测试新配置
5. **监控稳定** - 升级后观察日志和指标
6. **保留回滚路径** - 确保可以快速恢复旧配置
