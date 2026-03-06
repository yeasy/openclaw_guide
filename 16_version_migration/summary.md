## 第十六章 小结

## 核心概念

### 版本支持政策

```
v0.8  ├─ EOL (End of Life)，仅历史参考
v1.0  ├─ 维护期，仅安全补丁
v1.2  ├─ 主力版本，充分测试
v1.5  ├─ 最新版本，推荐使用
v1.6+ └─ 未来版本（TBD）
```

### 版本间的兼容性

**关键原则**：
- **同主版本**（如 v1.0 → v1.2）：通常向后兼容
- **跨主版本**（如 v0.8 → v1.0）：需要迁移工具
- **多版本跨越**（如 v0.8 → v1.5）：逐级迁移

## 常见升级路径

### 路径1：v1.0 → v1.2（推荐）

**步骤**：
```bash
openclaw upgrade --version v1.2
openclaw doctor  # 验证
```

**时间**：< 15分钟

**关键变更**：
- memory.compactOnTurns → memory.compactionMode
- requireMention 改位置

### 路径2：v0.8 → v1.5（跨越式）

**步骤**：
```bash
# 自动迁移
openclaw config migrate --target v1.5 --backup yes

# 验证
openclaw config validate

# 升级
openclaw upgrade --version v1.5

# 测试
openclaw doctor --deep
```

**时间**：1-2小时

### 路径3：生产环境滚动升级

```bash
# 1. 金丝雀：10%流量
kubectl patch deploy openclaw-v1.5 --replicas 1
sleep 2h

# 2. 扩大：50%流量
kubectl patch deploy openclaw-v1.5 --replicas 5

# 3. 全量：100%流量
kubectl patch deploy openclaw-v1.5 --replicas 10

# 4. 监控：24h
openclaw metrics watch --period 24h

# 5. 确认
```

## 字段变更要点

### 最高频变更

**v1.0 → v1.2**
```json
// 旧
"tools": ["tool1", "tool2"]

// 新
"toolGroups": { "default": ["tool1", "tool2"] }
```

**v1.2 → v1.5**
```json
// 旧
"model": "claude-opus"

// 新
"models": [{ "model": "claude-opus", "weight": 1.0 }]
```

**v0.8 → v1.0**（最大的变化）
```json
// 旧：单Agent
"agent": { "name": "bot", "model": "..." }

// 新：多Agent
"agents": {
  "bot": { "name": "bot", "model": "..." }
}
```

## 自动迁移工具

### 使用方式

```bash
# 完全自动化（推荐）
openclaw config migrate auto

# 指定目标版本
openclaw config migrate --target v1.5

# 干跑（不修改文件）
openclaw config migrate --dry-run

# 详细日志
openclaw config migrate --verbose
```

### 工具功能

✓ 自动检测当前版本
✓ 逐级迁移（v0.8→v1.0→v1.2→v1.5）
✓ 自动备份原配置
✓ 验证迁移结果
✓ 生成变更报告
✓ 故障时支持回滚

## 最佳实践

### 升级前

- [ ] 备份配置：`cp -r ~/.openclaw ~/.openclaw.backup`
- [ ] 检查版本：`openclaw version`
- [ ] 完整诊断：`openclaw doctor --deep`
- [ ] 阅读变更日志

### 升级中

- [ ] 使用自动迁移工具
- [ ] 验证配置合法性
- [ ] 在测试环境充分验证
- [ ] 生产环境使用滚动升级

### 升级后

- [ ] 再次运行诊断
- [ ] 监控日志中的警告
- [ ] 验证关键功能
- [ ] 收集性能基线数据

## 回滚策略

如果升级失败或发现问题：

```bash
# 方案1：恢复备份
openclaw config restore ~/.openclaw.backup

# 方案2：降级二进制
openclaw upgrade --version v1.0

# 方案3：完整回滚
rm -rf ~/.openclaw
cp -r ~/.openclaw.backup ~/.openclaw
openclaw gateway restart
```

## 常见升级问题

### Q: 升级会停机吗？

**A**：取决于策略
- 开发环境：无停机（秒级重启）
- 生产环境：使用滚动升级实现零停机

### Q: 配置能直接用吗？

**A**：取决于版本跨度
- 同次版本：直接用（v1.2→v1.3）
- 跨次版本：自动迁移（v1.0→v1.2）
- 跨主版本：手工或自动迁移（v0.8→v1.0）

### Q: 大量自定义配置怎么办？

**A**：OpenClaw支持：
- 自动转换脚本处理结构变更
- 变更报告显示所有改动
- 自定义脚本扩展自动化
- 支持团队可提供协助

## 进阶：自定义迁移扩展

如果自动工具不满足需求，可自定义：

```javascript
class CustomMigrator extends ConfigMigrator {
  transformCustomField(config) {
    // 自定义转换逻辑
    if (config.myField) {
      config.myField = transformValue(config.myField);
    }
    return config;
  }
}

const migrator = new CustomMigrator();
await migrator.migrate(configPath);
```

## 版本信息查询

```bash
# 查看当前版本
openclaw version

# 查看可用版本
openclaw version --available

# 查看版本详情
openclaw version --info

# 查看变更日志
openclaw changelog --version v1.5
openclaw changelog --range v1.0..v1.5
```

## 下一步

升级完成后：
1. **第17章**：利用新诊断工具排查潜在问题
2. **第15章**：优化配置以充分利用新特性
3. **第18章**：集成新的第三方工具和服务

## 支持与资源

- **完整变更日志**：项目CHANGELOG.md
- **兼容性表**：16.1.5
- **自动迁移工具**：openclaw config migrate
- **技术支持**：support@openclaw.example.com
