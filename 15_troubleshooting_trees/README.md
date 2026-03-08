# 第十五章：常见故障的诊断决策树

本章通过决策树的形式，提供系统化的故障排查流程，帮助工程师快速定位和解决 OpenClaw 运行中的常见问题。通过本章，你将掌握"快速诊断 → 精确定位 → 有效解决"的故障排查方法论。

> 快速参考：[附录 C 排障检查清单](../appendix/troubleshooting_checklist.md)提供按故障类型分类的速查表，[附录 F 命令速查表](../appendix/command_cheatsheet.md)列出所有诊断命令的完整语法。

## 本章内容导读

本章包括以下几个小节：

### 15.1 故障诊断决策树与工具

包含 6 个完整的故障诊断决策树，覆盖：
- 启动失败诊断（进程启动、端口占用、配置错误等）
- 消息无法接收诊断（Lark、Slack、邮件、通用渠道等）
- 模型调用异常诊断（认证、速率限制、API 故障、超时等）
- 工具执行失败诊断（权限、执行错误、无返回等）
- 会话与内存异常诊断（上下文丢失、记忆混乱、内存溢出等）
- 性能退化诊断（CPU、内存、磁盘 I/O、网络延迟等）

### 15.2 高并发故障诊断决策树与优化指南

针对高并发场景下特有的故障现象：
- 并发限制触发
- 连接池耗尽
- 队列堆积
- 级联故障

### 15.3 本章小结

诊断最佳实践与自检清单。

## 学习目标

完成本章的阅读后，你将能够：
1. **快速诊断**：面对问题时，能够按系统方法逐步排除可能性。
2. **定位根因**：通过决策树找到问题的真实原因。
3. **执行修复**：根据诊断结果，实施合适的解决方案。
4. **预防问题**：学习如何在问题发生前识别风险信号。

## 使用指南

### 第一步：确定症状

看到问题后，确定属于哪个大类：

```
启动失败？      → 决策树 1
收不到消息？    → 决策树 2
模型返回错误？  → 决策树 3
工具执行失败？  → 决策树 4
丢失历史/内存？ → 决策树 5
响应变慢？      → 决策树 6
```

### 第二步：按照决策树逐步诊断

每个决策树都是 **是/否** 分支，逐步排除可能性：

```
入口问题
  ↓
  检查 A 【是/否】
    ↓         ↓
   是        否
    ↓         ↓
执行A方案    检查B
    ↓         ↓
    ·        【是/否】
    ·         ·
    ·         ·
```

### 第三步：执行诊断命令

每个分支都提供具体的命令：

```bash
# 例如：检查Port占用
sudo lsof -i :18789

# 例如：验证配置
openclaw config validate

# 例如：查看日志
openclaw logs --follow --filter error
```

### 第四步：实施解决方案

诊断树引导到解决方案：
- 修改配置
- 重启服务
- 更新凭证
- 扩容资源
- ...

## 快速诊断命令

### 一键诊断

```bash
# 完整系统诊断（推荐首选）
openclaw doctor --deep

# 输出内容包括：
# - 配置文件检查
# - 依赖检查
# - 网络连接检查
# - 工具可用性检查
# - 建议的修复方案
```

### 按组件诊断

```bash
openclaw doctor gateway      # Gateway连接
openclaw doctor models       # 模型配置与连接
openclaw doctor channels     # 所有渠道（Lark/Slack等）
openclaw doctor tools        # 工具配置与权限
openclaw doctor database     # 数据库连接
```

### 日志追踪

```bash
# 实时查看所有日志
openclaw logs --follow

# 仅看错误
openclaw logs --follow --level error

# 特定组件的日志
openclaw logs --follow --filter "model.*"
openclaw logs --follow --filter "tool.*"
openclaw logs --follow --filter "lark.*"
```

### 性能监控

```bash
# 查看关键性能指标
openclaw metrics --period 5m
openclaw metrics --metric latency
openclaw metrics --metric throughput

# 导出详细报告
openclaw metrics export --format json > metrics.json
```

### 配置验证

```bash
# 验证配置有效性
openclaw config validate

# 查看特定配置项
openclaw config get agents.work-assistant
openclaw config get tools.github_pr_analyzer

# 查看配置Schema（用于查询可用字段）
openclaw config schema show tool github_pr_analyzer
```

### 权限检查

```bash
# 查看用户权限
openclaw permission show --user user@example.com

# 测试特定操作的权限
openclaw permission test --user user@example.com \
                          --tool github_pr_analyzer \
                          --action read
```

### 会话诊断

```bash
# 列出所有活跃会话
openclaw session list

# 查看特定会话的详情
openclaw session dump --id session-abc123

# 清除缓存
openclaw session clear-cache
```

### 收集诊断包（用于反馈）

```bash
# 生成包含日志、配置（脱敏）、系统信息的完整诊断包
openclaw diag export --output openclaw-diag-$(date +%Y%m%d-%H%M%S).zip

# 用于提交issue或寻求支持
```

## 常见问题的快速解决

### “消息无法接收”

最常见原因排序（按概率）：

1. **飞书应用未发布** → 解决：在飞书开放平台点击“发布”
2. **事件订阅未启用** → 解决：启用长连接方式的事件订阅
3. **Webhook URL错误** → 解决：确认OpenClaw Gateway外网可访问
4. **群聊未启用/设置** → 解决：检查openclaw.json中的channel配置
5. **消息路由规则** → 解决：检查是否设置了正确的@机器人或关键词

### “模型调用失败”

最常见原因排序：

1. **API 密钥无效** → 解决：检查并更新环境变量中的密钥
2. **速率限制** → 解决：检查API额度，或实施本地速率限制
3. **网络连接** → 解决：测试ping api.anthropic.com，检查防火墙
4. **账户额度耗尽** → 解决：检查API额度，升级账户或重新注册
5. **模型参数错误** → 解决：检查模型名称、Token限制等

### “内存溢出/OOM”

最常见原因排序：

1. **上下文未压缩** → 解决：启用memory.compactionMode
2. **缓存过大** → 解决：设置缓存TTL和大小限制
3. **内存泄漏** → 解决：升级补丁版本，检查已知泄漏
4. **并发太高** → 解决：增加maxConcurrentRequests限制或加机器
5. **会话过多** → 解决：增加session清理策略

## 诊断树与命令的映射

每个诊断树中的分支都对应具体命令：

```
决策树 1：启动失败
  │
  ├─ 进程无法启动
  │   └─ 运行: openclaw doctor gateway
  │
  ├─ 配置文件格式错误
  │   └─ 运行: openclaw config validate
  │
  └─ 权限不足
      └─ 运行: ls -la ~/.openclaw
```

## 最佳实践

### 日常维护

- **每周** 运行：`openclaw doctor --deep` 并检查输出
- **每天** 监控：关键指标（延迟、错误率、成本）
- **每月** 审计：日志、权限配置、安全更新

### 故障排查

1. **首先**：运行 `openclaw doctor --deep`
2. **其次**：按症状找到对应的决策树
3. **第三**：执行诊断树中的命令逐步排除
4. **最后**：如果仍无法解决，收集诊断包并提交支持

### 预防性诊断

- 启用自动化监控与告警
- 定期进行健康检查
- 保留完整的日志记录（用于事后分析）
- 建立故障恢复的标准操作流程（SOP）

## 下一步

诊断和修复问题后，建议：
1. **第14章**：了解类似案例如何避免此类问题
2. **第15章**：优化性能，避免性能相关故障
3. **第18章**：利用更多工具提升系统可靠性

## 支持与反馈

如果诊断树未能解决问题：
- 收集诊断包：`openclaw diag export`
- 提交issue：附带诊断包和详细的问题描述
- 联系支持：support@openclaw.example.com
