# 迁移到 uv + pyproject.toml 指南

本文档说明如何从传统的 `Makefile` + `requirements.txt` 迁移到现代的 `uv` + `pyproject.toml` 工作流。

## 为什么要迁移？

### uv + pyproject.toml 的优势

| 特性 | Makefile + pip | uv + pyproject.toml |
|------|---------------|---------------------|
| 安装速度 | 慢（几分钟） | 极快（10-100倍） |
| 依赖锁定 | ❌ 无 | ✅ 自动生成 `uv.lock` |
| 虚拟环境 | 手动管理 | ✅ 自动创建和管理 |
| 项目元数据 | 分散 | ✅ 统一在 `pyproject.toml` |
| Python标准 | ❌ 非标准 | ✅ PEP 518/621 标准 |
| 可选依赖 | ❌ 不支持 | ✅ 支持（如多模态功能） |
| 跨平台 | ⚠️ Windows 支持差 | ✅ 完美跨平台 |

### 实际性能对比

```bash
# 安装所有依赖的时间对比
pip install -r requirements.txt    # ~3-5 分钟
uv sync                            # ~10-30 秒（首次）
uv sync                            # ~1-2 秒（后续）
```

## 迁移步骤

### 1. 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv

# 验证安装
uv --version
```

### 2. 安装依赖（自动迁移）

```bash
# 进入项目目录
cd emotional_chat

# uv 会自动读取 pyproject.toml 并安装依赖
uv sync
```

**发生了什么？**
- ✅ uv 自动创建虚拟环境（`.venv/`）
- ✅ 读取 `pyproject.toml` 中的依赖列表
- ✅ 解析依赖树并安装所有包
- ✅ 生成 `uv.lock` 锁文件（确保环境一致）

### 3. 使用新命令

#### 命令对照表

| 功能 | 旧命令（Makefile） | 新命令（uv） |
|------|-------------------|-------------|
| 安装依赖 | `make install` | `uv sync` |
| 运行后端 | `make run` | `uv run emotional-chat run` |
| 数据库升级 | `make db-upgrade` | `uv run emotional-chat db upgrade` |
| 检查数据库 | `make db-check` | `uv run emotional-chat db check` |
| 初始化RAG | `make rag-init` | `uv run emotional-chat rag init` |
| 测试RAG | `make rag-test` | `uv run emotional-chat rag test` |
| 查看帮助 | `make help` | `uv run emotional-chat --help` |

#### 运行脚本

```bash
# 旧方式
python test_agent.py

# 新方式（自动使用虚拟环境）
uv run python test_agent.py
```

## 新功能特性

### 1. 可选依赖组

现在可以根据需要安装不同的依赖组：

```bash
# 仅安装基础依赖
uv sync

# 安装基础 + 多模态功能（语音识别、图像处理）
uv sync --extra multimodal

# 安装基础 + 开发工具
uv sync --extra dev

# 安装所有依赖
uv sync --all-extras
```

### 2. 自动虚拟环境管理

```bash
# uv 自动创建和激活虚拟环境
uv run python test_agent.py        # 自动使用 .venv

# 手动激活虚拟环境（如需要）
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. 依赖锁定

```bash
# uv.lock 确保环境一致性
uv sync              # 根据 uv.lock 安装精确版本

# 更新依赖到最新版本
uv sync --upgrade

# 添加新依赖
uv add requests      # 自动更新 pyproject.toml 和 uv.lock

# 移除依赖
uv remove requests
```

### 4. 统一的 CLI 工具

新增 `emotional-chat` 命令行工具：

```bash
# 查看所有命令
uv run emotional-chat --help

# 运行服务
uv run emotional-chat run

# 数据库管理
uv run emotional-chat db upgrade
uv run emotional-chat db downgrade
uv run emotional-chat db check
uv run emotional-chat db current
uv run emotional-chat db history
uv run emotional-chat db reset

# RAG管理
uv run emotional-chat rag init
uv run emotional-chat rag test
uv run emotional-chat rag demo
```

## 向后兼容

### Makefile 仍然可用

如果你习惯使用 Makefile，**所有旧命令仍然有效**：

```bash
make install       # 仍然有效
make run           # 仍然有效
make db-upgrade    # 仍然有效
```

### requirements.txt 保留

`requirements.txt` 文件会继续保留，以便：
- 在不支持 `pyproject.toml` 的旧环境中使用
- 与 Docker 等工具兼容
- 作为依赖的参考文档

## 常见问题

### Q1: 如何在现有虚拟环境中使用 uv？

```bash
# uv 会自动检测并使用现有虚拟环境
source .venv/bin/activate  # 或 Windows: .venv\Scripts\activate
uv sync
```

### Q2: uv.lock 文件是否需要提交到 Git？

**推荐提交 `uv.lock`**，这样可以确保团队成员使用完全相同的依赖版本。

```bash
# .gitignore 中不应该包含 uv.lock
git add uv.lock
git commit -m "添加依赖锁定文件"
```

### Q3: 如何在 CI/CD 中使用 uv？

```yaml
# GitHub Actions 示例
- name: 安装 uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: 安装依赖
  run: uv sync

- name: 运行测试
  run: uv run pytest
```

### Q4: 如何更新单个包？

```bash
# 更新特定包
uv add --upgrade langchain

# 更新所有包
uv sync --upgrade
```

### Q5: 我不想用 uv，可以继续用 pip 吗？

完全可以！项目仍然完全支持传统方式：

```bash
pip install -r requirements.txt
python run_backend.py
```

### Q6: 虚拟环境在哪里？

uv 默认在项目根目录创建 `.venv/`：

```bash
# 查看虚拟环境路径
ls -la .venv

# 手动激活（可选）
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Q7: 如何在 Docker 中使用 uv？

更新 `Dockerfile`：

```dockerfile
# 安装 uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# 安装依赖
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# 运行应用
CMD ["uv", "run", "emotional-chat", "run"]
```

## 性能优化建议

### 1. 使用国内镜像源（可选）

编辑 `pyproject.toml`：

```toml
[tool.uv.sources]
[[tool.uv.index]]
url = "https://mirrors.aliyun.com/pypi/simple/"
name = "aliyun"
```

### 2. 缓存加速

uv 自动缓存下载的包，后续安装会更快：

```bash
# 查看缓存
uv cache info

# 清理缓存（如需要）
uv cache clean
```

### 3. 并行安装

uv 默认并行安装依赖，无需额外配置。

## 故障排除

### 问题：uv sync 失败

```bash
# 清理并重试
rm -rf .venv uv.lock
uv sync
```

### 问题：找不到 emotional-chat 命令

```bash
# 确保已安装项目
uv sync

# 使用完整路径
uv run emotional-chat --help

# 或激活虚拟环境
source .venv/bin/activate
emotional-chat --help
```

### 问题：Windows 上 pysqlite3-binary 不可用

这是已知问题，代码已经处理：

```python
# backend/main.py 会自动使用内置 sqlite3
sys.modules['pysqlite3'] = __import__('sqlite3')
```

无需额外配置。

## 总结

迁移到 `uv` + `pyproject.toml` 后，你将获得：

- ✅ **极速安装**：10-100倍提速
- ✅ **依赖锁定**：环境一致性保证
- ✅ **自动虚拟环境**：无需手动管理
- ✅ **标准化**：符合 Python 生态标准
- ✅ **更好的开发体验**：统一的 CLI 工具
- ✅ **向后兼容**：旧命令仍然有效

**开始迁移**：

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 进入项目
cd emotional_chat

# 3. 安装依赖
uv sync

# 4. 运行项目
uv run emotional-chat run
```

就是这么简单！🚀

## 参考资源

- [uv 官方文档](https://docs.astral.sh/uv/)
- [PEP 621 - 项目元数据标准](https://peps.python.org/pep-0621/)
- [pyproject.toml 规范](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
