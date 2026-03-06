# 第十六章：版本映射与升级指南

本章提供跨版本配置兼容性说明、自动迁移工具、以及平滑升级路径，确保用户能够无风险地升级 OpenClaw 到最新版本。通过本章，你将掌握如何在生产环境中安全、高效地实施版本升级。

## 本章内容导读

本章包括以下几个小节：

### 16.1 版本映射与配置字段变更记录

系统化的版本变更文档，包括：
- **版本时间线**：从 v0.8 到 v1.5 的演进
- **字段变更对照表**：详细的字段映射与变更说明
- **废弃字段指南**：每个版本的废弃字段与替代方案
- **自动迁移脚本**：一键升级配置文件
- **兼容性表**：版本间的可读写关系

### 16.2 本章小结

升级检查单与最佳实践。

## 学习目标

完成本章的阅读后，你将能够：
1. **理解变更**：清晰地了解版本间的配置变更。
2. **规划升级**：选择合适的升级策略（直接升级、逐级升级、灰度发布）。
3. **执行迁移**：使用自动化工具进行配置迁移。
4. **验证成功**：确保升级后系统正常运行。

## 快速参考

### 支持政策

- **主版本（Major）**：推荐6个月内升级，超期可能有安全风险
- **次版本（Minor）**：2个版本内向后兼容
- **补丁版本（Patch）**：完全兼容

### 版本支持期

```
v0.8  ├─ 已停止支持（2024-Q2）
v1.0  ├─ 进入维护期（仅安全补丁）
v1.2  ├─ 主力支持版本
v1.5  ├─ 最新版本（推荐）
v1.6+ │  未来版本（TBD）
```

## 常见升级场景

### 场景1：从v1.0升级到v1.2（推荐）

**兼容性**：✓ 配置可直接读取，无需转换

```bash
# 仅需更新二进制
openclaw upgrade --version v1.2

# 验证
openclaw version  # 应显示v1.2
openclaw doctor   # 应全部通过
```

**关键变更**：
- `memory.compactOnTurns` → `memory.compactionMode`
- `channels.*.requireMention` 改为 `channels.*.routing[].conditions.requireMention`

**升级时间**：< 15分钟

### 场景2：从v0.8升级到v1.5（跨越式升级）

**兼容性**：✗ 需要逐级迁移

```bash
# 步骤1：自动迁移配置
openclaw config migrate --input ~/.openclaw/openclaw.json \
                        --target v1.5 \
                        --backup yes

# 步骤2：验证迁移结果
openclaw config validate

# 步骤3：更新二进制
openclaw upgrade --version v1.5

# 步骤4：测试
openclaw doctor --deep
```

**升级时间**：1-2小时（含测试）

### 场景3：企业生产环境的金丝雀升级

```bash
# 1. 在测试环境验证
TEST_ENV=true openclaw upgrade --version v1.5

# 2. 10%流量灰度测试
kubectl patch deploy openclaw \
  -p '{"spec":{"template":{"metadata":{"annotations":{"version":"v1.5"}}}}}'
sleep 2h  # 观察

# 3. 50%流量扩大
# 4. 100%流量全量发布
# 5. 监控24h，无问题后确认
```

## 字段变更速查

### 最常见的变更

```
v1.0 → v1.2:
  agent.tools: ['tool1']
    ↓ 支持工具组
  agent.toolGroups: { default: ['tool1'] }

v1.2 → v1.5:
  agents.*.model: 'claude-opus'
    ↓ 支持多模型fallback
  agents.*.models: [
    { model: 'claude-opus', weight: 1.0 }
  ]
```

完整的对照表见章节16.1.3

## 自动迁移工具

### 一键迁移

```bash
# 最简单的方式：自动检测并迁移到最新版本
openclaw config migrate auto

# 或指定目标版本
openclaw config migrate --target v1.5

# 生成变更报告（不执行变更）
openclaw config migrate --dry-run
```

### 故障排查

如果迁移失败：

```bash
# 查看详细错误
openclaw config migrate --verbose

# 验证配置结构
openclaw schema validate ~/.openclaw/openclaw.json

# 恢复备份
openclaw config restore ~/.openclaw/openclaw.json.backup.v1.0
```

## 升级检查单

**升级前**：
- [ ] 备份现有配置：`cp -r ~/.openclaw ~/.openclaw.backup`
- [ ] 检查当前版本：`openclaw version`
- [ ] 运行诊断：`openclaw doctor`
- [ ] 查看变更日志：相关版本的 CHANGELOG.md

**升级过程中**：
- [ ] 停止生产流量（或灰度更新）
- [ ] 执行自动迁移
- [ ] 验证配置有效性
- [ ] 更新二进制
- [ ] 启动并验证

**升级后**：
- [ ] 运行完整诊断：`openclaw doctor --deep`
- [ ] 测试关键功能
- [ ] 监控错误日志：`openclaw logs --filter error`
- [ ] 恢复生产流量

## 常见问题

**Q: 升级会造成停机吗？**

A: 不一定。取决于升级策略：
- 开发环境：无停机时间（仅秒级重启）
- 生产环境：可实施滚动更新、金丝雀发布等零停机策略

**Q: 旧配置文件能直接用吗？**

A: 取决于版本跨度：
- v1.2 → v1.5：可直接用（兼容）
- v1.0 → v1.5：需要迁移（自动工具可处理）
- v0.8 → v1.5：强烈建议重新配置（变化太大）

**Q: 如果迁移出错怎么办？**

A: 有完整的回滚方案：
1. 恢复备份：`openclaw config restore`
2. 降级二进制：`openclaw upgrade --version v1.0`
3. 重新启动：`openclaw gateway start`

**Q: 企业有大量自定义配置，迁移复杂吗？**

A: OpenClaw提供工具支持：
- 配置转换脚本：自动处理结构变更
- 变更报告：生成详细的改动说明
- 验证工具：发现潜在问题
- 支持团队：可提供定制化帮助

## 下一步

升级后，建议：
1. 参考 **第17章故障诊断** 了解新版本特性
2. 参考 **第15章性能优化** 利用新特性优化成本
3. 参考 **第18章集成指南** 接入新的第三方工具

## 更新日志

所有版本的详细变更见项目的 CHANGELOG.md 文件。

## 技术支持

- 升级失败：`openclaw support file-issue --category upgrade`
- 配置问题：检查 16.1.3 的字段变更对照表
- 兼容性疑问：查看 16.1.5 的兼容性表
