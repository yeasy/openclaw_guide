## 附录H：环境自检工具

以下是前置诊断脚本 `check_env.sh`，用于验证 OpenClaw 的核心运行依赖。

```bash
#!/bin/bash
echo "=== OpenClaw 环境自检 ==="
if command -v node >/dev/null 2>&1; then
  node_version="$(node -p 'process.versions.node')"
  node_major="${node_version%%.*}"
  node_rest="${node_version#*.}"
  node_minor="${node_rest%%.*}"
  node_patch="${node_rest#*.}"
  echo "Node.js: v${node_version}"
  # 官方支持线：22.22.3+ / 24.15+ / 25.9+（含 26），Node 23 不受支持
  node_supported=0
  case "$node_major" in
    22)
      if [ "$node_minor" -gt 22 ] || { [ "$node_minor" -eq 22 ] && [ "$node_patch" -ge 3 ]; }; then
        node_supported=1
      fi
      ;;
    23) node_supported=0 ;;
    24) [ "$node_minor" -ge 15 ] && node_supported=1 ;;
    25) [ "$node_minor" -ge 9 ] && node_supported=1 ;;
    *)  [ "$node_major" -ge 26 ] && node_supported=1 ;;
  esac
  if [ "$node_supported" -eq 0 ]; then
    echo "警告: 当前 Node 不在官方支持线内（需 22.22.3+ / 24.15+ / 25.9+，Node 23 不受支持）；建议升级到 Node 26。"
  elif [ "$node_major" -lt 26 ]; then
    echo "提示: 当前版本受支持；新安装推荐 Node 26（官方 CI 与发布流程仍固定 Node 24）。"
  fi
else
  echo "警告: 未安装 Node.js（推荐 Node 26；官方支持线为 22.22.3+ / 24.15+ / 25.9+）"
fi
npm --version || echo "提示: 未安装 npm。如果不使用自动化脚本安装，这是必需项"
docker --version || echo "提示: 未安装 Docker (如使用容器化部署则是必需项)"

echo "测试网络连通（官方安装脚本）..."
curl -fsSL -m 5 -o /dev/null -w "install script: %{http_code}\n" https://openclaw.ai/install.sh

echo "测试运行期网络（模型供应商 API，以 OpenAI 为例，可替换为你的供应商）..."
if [ -n "${OPENAI_API_KEY:-}" ]; then
  curl -sS -m 10 -o /dev/null -w "llm provider: %{http_code}\n" https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
else
  curl -sS -m 10 -o /dev/null -w "llm provider: %{http_code}\n" https://api.openai.com/v1/models
fi
echo "提示: 200 表示鉴权通过；401/403 多为无 Key/无权限但网络可达。"
echo "如果启用了 OpenClaw 托管代理，shell curl 不会验证运行时代理路径；请检查 proxy.enabled / proxy.proxyUrl 或 OPENCLAW_PROXY_URL，并运行 openclaw proxy validate。"
echo "自检完成"
```

**正常环境下的预期输出**：

```text
=== OpenClaw 环境自检 ===
Node.js: v26.2.0
10.9.2
Docker version 27.3.1, build ce1223035a
测试网络连通（官方安装脚本）...
install script: 200
测试运行期网络（模型供应商 API，以 OpenAI 为例，可替换为你的供应商）...
llm provider: 200
提示: 200 表示鉴权通过；401/403 多为无 Key/无权限但网络可达。
如果启用了 OpenClaw 托管代理，shell curl 不会验证运行时代理路径；请检查 proxy.enabled / proxy.proxyUrl 或 OPENCLAW_PROXY_URL，并运行 openclaw proxy validate。
自检完成
```

**常见异常场景及排查**：

| 输出 | 含义 | 排查方向 |
|------|------|---------|
| `警告: 未安装 Node.js` | Node.js 未安装或不在 PATH | 执行 `nvm install 26`（推荐）或 `nvm install 24` |
| `警告: 当前 Node 不在官方支持线内` | 当前 Node 版本过低，或落在不受支持的 Node 23 上 | 升级到 Node 26，或至少升级到 22.22.3+ / 24.15+ / 25.9+ |
| `install script: 000` | 无法连接 openclaw.ai | 检查网络/代理/DNS 设置 |
| `llm provider: 401` | API Key 无效或未设置 | 检查 `$OPENAI_API_KEY` 环境变量 |
| `llm provider: 403` | API Key 无权限 | 确认 API Key 对应账户有可用额度 |
