## 附录 H：环境自检工具

以下是前置诊断脚本 `check_env.sh`，用于验证 OpenClaw 的核心运行依赖。

```bash
#!/bin/bash
echo "=== OpenClaw 环境自检 ==="
if command -v node >/dev/null 2>&1; then
  node_version="$(node -p 'process.versions.node')"
  node_major="${node_version%%.*}"
  node_rest="${node_version#*.}"
  node_minor="${node_rest%%.*}"
  node_patch="${node_rest#*.}"; node_patch="${node_patch%%[!0-9]*}"
  echo "Node.js: v${node_version}"
  # 官方支持线：24.16+ / 26.1+；Node 22、23、25 与 26.0 不受支持
  node_supported=0
  case "$node_major" in
    24) [ "$node_minor" -ge 16 ] && node_supported=1 ;;
    26) [ "$node_minor" -ge 1 ] && node_supported=1 ;;
    *)  [ "$node_major" -ge 27 ] && node_supported=1 ;;
  esac
  if [ "$node_supported" -eq 0 ]; then
    echo "警告: 当前 Node 不在官方支持线内（需 24.16+ 或 26.1+，Node 22、23、25 不受支持）；建议升级到 Node 26。"
  elif [ "$node_major" -lt 26 ]; then
    echo "提示: 当前版本受支持；新安装推荐 Node 26（官方 CI 与 Linux 安装脚本使用 Node 24）。"
  fi
  # 安全补丁建议线：24.22.1+ / 26.12.1+（低于此线仍可运行，security audit 会报 runtime.node_security_patch）
  node_level=$(( node_minor * 1000 + ${node_patch:-0} ))
  if [ "$node_supported" -eq 1 ] && { { [ "$node_major" -eq 24 ] && [ "$node_level" -lt 22001 ]; } || { [ "$node_major" -eq 26 ] && [ "$node_level" -lt 12001 ]; }; }; then
    echo "提示: 建议升级到安全补丁版本 Node 24.22.1+ 或 26.12.1+。"
  fi
else
  echo "警告: 未安装 Node.js（推荐 Node 26；官方支持线为 24.16+ / 26.1+）"
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
Node.js: v26.12.1
11.20.0
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
| `警告: 当前 Node 不在官方支持线内` | 当前 Node 版本过低，或落在不受支持的 Node 22、23、25 上 | 升级到 Node 26（26.1+），或至少升级到 24.16+ |
| `提示: 建议升级到安全补丁版本` | Node 受支持，但低于官方建议的安全补丁线 | 升级到 Node 24.22.1+ 或 26.12.1+；Gateway 服务若用另一个 Node，需单独升级并重启 |
| `install script: 000` | 无法连接 openclaw.ai | 检查网络/代理/DNS 设置 |
| `llm provider: 401` | API Key 无效或未设置 | 检查 `$OPENAI_API_KEY` 环境变量 |
| `llm provider: 403` | API Key 无权限 | 确认 API Key 对应账户有可用额度 |
