## 附录：环境自检工具

以下是前置诊断脚本 `check_env.sh`，用于验证 OpenClaw 的核心运行依赖。

```bash
#!/bin/bash
echo "=== OpenClaw 环境自检 ==="
node --version || echo "警告: 未安装 Node.js（推荐 Node 24，最低 Node 22.16+）"
npm --version || echo "提示: 未安装 npm。如果不使用自动化脚本安装，这是必需项"
docker --version || echo "提示: 未安装 Docker (如使用容器化部署则是必需项)"

echo "测试网络连通（官方安装脚本）..."
curl -s -m 5 -o /dev/null -w "install script: %{http_code}\n" https://openclaw.ai/install.sh

echo "测试运行期网络（模型供应商 API，以 OpenAI 为例，可替换为你的供应商）..."
if [ -n "${OPENAI_API_KEY:-}" ]; then
  curl -sS -m 10 -o /dev/null -w "llm provider: %{http_code}\n" https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
else
  curl -sS -m 10 -o /dev/null -w "llm provider: %{http_code}\n" https://api.openai.com/v1/models
fi
echo "提示: 200 表示鉴权通过；401/403 多为无 Key/无权限但网络可达。"
echo "自检完成"
```


**正常环境下的预期输出**：

```text
=== OpenClaw 环境自检 ===
v22.12.0
10.2.3
Docker version 27.3.1, build ce1223035a
测试网络连通（官方安装脚本）...
install script: 200
测试运行期网络（模型供应商 API，以 OpenAI 为例，可替换为你的供应商）...
llm provider: 200
提示: 200 表示鉴权通过；401/403 多为无 Key/无权限但网络可达。
自检完成
```

**常见异常场景及排查**：

| 输出 | 含义 | 排查方向 |
|------|------|---------|
| `警告: 未安装 Node.js` | Node.js 未安装或不在 PATH | 执行 `nvm install 24`（推荐）或 `nvm install 22` |
| `install script: 000` | 无法连接 openclaw.ai | 检查网络/代理/DNS 设置 |
| `llm provider: 401` | API Key 无效或未设置 | 检查 `$OPENAI_API_KEY` 环境变量 |
| `llm provider: 403` | API Key 无权限 | 确认 API Key 对应账户有可用额度 |
