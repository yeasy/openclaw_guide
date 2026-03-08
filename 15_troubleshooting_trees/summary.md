## 第十五章 小结

## 诊断方法论

### 核心原则

**二分法逐步排除**：
- 从最可能的原因开始
- 通过是/否分支逐步缩小范围
- 每个分支都对应可执行的命令
- 最终导向具体的解决方案

### 六大故障类别

| 类别 | 症状 | 首选命令 | 难度 |
|------|------|---------|------|
| 启动失败 | 进程无法启动 | `openclaw doctor` | ⭐ |
| 消息接收 | 无消息流入 | `openclaw logs --filter channel` | ⭐⭐ |
| 模型调用 | API错误 | `openclaw logs --filter model` | ⭐⭐ |
| 工具执行 | 工具出错 | `openclaw permission test` | ⭐⭐⭐ |
| 内存/会话 | 上下文丢失 | `openclaw session dump` | ⭐⭐⭐ |
| 性能退化 | 响应变慢 | `openclaw metrics` | ⭐⭐⭐ |

## 快速诊断命令速查

### 一键诊断

```bash
openclaw doctor --deep
# 最全面的检查，包含所有组件

# 仅检查特定组件
openclaw doctor gateway      # Gateway
openclaw doctor models       # 模型
openclaw doctor channels     # 渠道
openclaw doctor tools        # 工具
openclaw doctor database     # 数据库
```

### 日志分析

```bash
# 实时日志追踪
openclaw logs --follow

# 按级别过滤
openclaw logs --follow --level error
openclaw logs --follow --level warn

# 按组件过滤
openclaw logs --filter "lark.*"       # Lark相关
openclaw logs --filter "model.*"      # 模型相关
openclaw logs --filter "tool.*"       # 工具相关

# 导出日志用于分析
openclaw logs export --format json --period last_7d > logs.json
```

### 性能分析

```bash
# 查看实时指标
openclaw metrics --period 5m

# 按指标查看
openclaw metrics --metric latency      # P50/P95/P99延迟
openclaw metrics --metric throughput   # 吞吐量
openclaw metrics --metric errors       # 错误率

# 导出性能报告
openclaw metrics export --format html > report.html
```

### 配置与权限

```bash
# 验证配置
openclaw config validate

# 查看配置项
openclaw config get agents.*.model

# 权限检查
openclaw permission show --user user@example.com
openclaw permission test --user user@example.com --tool github_pr_analyzer

# 会话诊断
openclaw session list
openclaw session dump --id session-xxx
```

## 常见故障的快速解决

### Top-5 最常见的问题

#### 1. “进程无法启动” (最常见)

**诊断**：`openclaw doctor`

**最可能原因**：
1. Port被占用 → `sudo lsof -i :18789` → 改端口或kill进程
2. 配置格式错误 → `openclaw config validate` → 修复JSON
3. 权限不足 → `ls -la ~/.openclaw` → `chown` 修复
4. 缺少依赖 → `openclaw doctor` 显示哪个缺失 → 安装

**解决时间**：5-15分钟

#### 2. “消息无法接收” (第二常见)

**诊断**：`openclaw logs --filter "channel.*"`

**最可能原因**（按概率）：
1. Lark应用未发布 → 在飞书平台点“发布”
2. 事件订阅未启用 → 启用长连接
3. Webhook URL错误 → 确认外网可访问
4. 群聊未启用 → 检查openclaw.json配置

**解决时间**：15-30分钟

#### 3. “模型调用失败” (模型问题)

**诊断**：`openclaw logs --filter "model.*failed"`

**最可能原因**（按概率）：
1. API 密钥无效 → 更新环境变量
2. 速率限制 → 检查quota，实施本地限流
3. 网络连接 → `ping api.anthropic.com`
4. 参数错误 → 检查model名称、token限制

**解决时间**：10-20分钟

#### 4. “工具执行出错” (工具问题)

**诊断**：`openclaw logs --filter "tool.*error"`

**最可能原因**（按概率）：
1. 权限不足 → `openclaw permission test` → 提升等级
2. 工具服务不可达 → `curl` 测试连接
3. Token过期 → 更新API凭证
4. 参数错误 → 检查Schema，验证参数值

**解决时间**：15-30分钟

#### 5. “响应变慢” (性能问题)

**诊断**：`openclaw metrics --metric latency`

**最可能原因**（按概率）：
1. 缓存命中率低 → 检查cache配置，增加TTL
2. 模型响应慢 → 检查API状态，考虑用更快的模型
3. 工具执行慢 → 检查外部服务性能，实施超时
4. CPU/内存压力 → 扩容或优化代码

**解决时间**：30分钟-2小时

## 诊断工作流

```
发现问题
  ├─ 【步骤1】确定症状类别
  │    └─ "进程启动" / "消息" / "模型" / "工具" / "性能" 等
  │
  ├─ 【步骤2】运行对应的诊断树
  │    └─ 从入口问题开始，按是/否分支进行
  │
  ├─ 【步骤3】执行每个分支的诊断命令
  │    └─ 查看输出，判断是哪一分支
  │
  └─ 【步骤4】实施解决方案
       └─ 修改配置 / 重启服务 / 更新凭证 等

验证修复
  └─ 运行对应的验证命令
       └─ 通常是 openclaw doctor 或实际功能测试
```

## 诊断工具的最佳实践

### 日常维护（预防故障）

**每周**：
```bash
openclaw doctor --deep  # 检查系统健康度
```

**每天**：
```bash
# 检查错误日志
openclaw logs --filter error --level error

# 监控关键指标
openclaw metrics --metric error_rate
openclaw metrics --metric latency
```

**每月**：
```bash
# 完整的审计与性能分析
openclaw metrics export --period 30d --format html > monthly_report.html
```

### 故障排查（发现问题后）

**第一步**（< 5分钟）：
```bash
openclaw doctor --deep
# 这通常会自动发现问题并提供建议
```

**第二步**（5-15分钟）：
```bash
# 如果doctor没有直接定位，使用决策树
# 找到对应的诊断树，按步骤执行

openclaw logs --follow  # 实时监看日志
```

**第三步**（15-30分钟）：
```bash
# 如果仍未解决，收集诊断信息并上报

openclaw diag export --output diag.zip
# 包含脱敏配置、日志、系统信息等
```

## 故障优先级与处理

```
P0 (紧急，立即处理)
├─ 系统完全不可用
├─ 数据丢失
└─ 安全漏洞
    → 处理时间：15分钟内

P1 (高，今天处理)
├─ 主要功能受损
├─ 消息无法处理
└─ 模型调用全部失败
    → 处理时间：2小时内

P2 (中，本周处理)
├─ 部分功能受损
├─ 性能下降
└─ 非关键工具失败
    → 处理时间：1天内

P3 (低，优化改进)
├─ 功能完全正常
├─ 优化建议
└─ 文档补充
    → 处理时间：灵活
```

## 进阶：自动化诊断

对于企业用户，可实施自动化诊断：

```bash
# 定时运行诊断（每小时）
*/60 * * * * openclaw doctor --json | \
  curl -X POST http://monitoring:8080/health-check

# 自动告警
openclaw metrics watch --threshold 2000 --metric latency \
  --on-breach "send_alert"
```

## 相关资源

- **决策树全图**：15.1章的Mermaid图
- **命令参考**：15.1.7 快速诊断命令参考
- **知识库**：常见问题解决方案（可搜索）
- **社区论坛**：用户经验分享

## 下一步

解决问题后，建议：
1. **第14章**：学习相似案例的预防措施
2. **第15章**：优化性能，避免后续性能问题
3. **第18章**：利用更多工具和服务提升稳定性

## 支持与反馈

无法解决的问题：
1. 收集诊断包：`openclaw diag export`
2. 提交Issue：附带诊断包和完整问题描述
3. 联系支持：support@openclaw.example.com
