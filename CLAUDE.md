# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于**通义千问 + Agent架构 + RAG知识库**的智能情感支持聊天机器人系统。

**技术栈**：
- 后端：Python 3.10+, FastAPI, LangChain
- 前端：React 18, Styled Components
- 数据库：MySQL 8.0 (关系数据), ChromaDB (向量数据)
- LLM：阿里云通义千问 (Qwen)

## 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0
- 阿里云通义千问 API Key

## 常用命令

### 后端开发

```bash
# 安装依赖（推荐使用 uv，比 pip 快 10-100 倍）
uv sync                      # 安装所有依赖并创建虚拟环境
uv sync --extra multimodal   # 安装依赖 + 多模态功能（语音、图像）
uv sync --extra dev          # 安装依赖 + 开发工具
uv sync --all-extras         # 安装所有依赖（包含所有可选功能）

# 运行后端服务（包含自动构建知识库和RAG）
uv run emotional-chat run    # 服务运行在 http://localhost:8000
                            # API文档: http://localhost:8000/docs

# 数据库管理
uv run emotional-chat db upgrade    # 升级数据库到最新版本（推荐首次安装时执行）
uv run emotional-chat db downgrade  # 降级数据库一个版本
uv run emotional-chat db check      # 检查数据库连接
uv run emotional-chat db current    # 查看当前数据库版本
uv run emotional-chat db history    # 查看迁移历史
uv run emotional-chat db reset      # 重置数据库（危险！会清空所有数据）

# RAG知识库管理
uv run emotional-chat rag init      # 初始化RAG知识库
uv run emotional-chat rag test      # 测试RAG系统（需要后端服务运行）
uv run emotional-chat rag demo      # 演示RAG效果对比

# 查看所有命令
uv run emotional-chat --help

# 兼容：也可以使用传统方式（不推荐）
# make install / make run / make db-upgrade 等命令仍然可用
```

### 前端开发

```bash
cd frontend
npm install                  # 安装依赖
npm start                    # 启动开发服务器（运行在 http://localhost:3000）
npm run build                # 构建生产版本
npm test                     # 运行测试
```

### 测试命令

```bash
# 测试Agent模块
uv run python test_agent.py

# 测试Agent工具
uv run python test_agent_tools.py

# 测试Python 3.10兼容性
uv run python test_python310.py

# 演示Agent功能
uv run python demo_agent.py

# 运行完整测试套件（如果有）
uv run pytest
```

### Docker部署

```bash
cp config.env.example config.env
# 编辑 config.env 配置
docker-compose up -d         # 启动所有服务
docker-compose down          # 停止所有服务
```

## 项目架构

### 分层架构

```
┌─────────────────────────────────────┐
│         路由层 (Routers)             │  API接口定义
├─────────────────────────────────────┤
│         服务层 (Services)            │  业务逻辑
├─────────────────────────────────────┤
│         核心层 (Modules)             │  Agent、RAG、LLM、Intent核心模块
├─────────────────────────────────────┤
│         数据层 (Database)            │  MySQL + ChromaDB
└─────────────────────────────────────┘
```

### 模块化结构

项目采用**模块化插件式架构**，核心模块位于 `backend/modules/`：

- **Agent模块** (`modules/agent/`)：Agent智能核心系统
  - Agent Core：核心控制器，协调所有模块
  - Memory Hub：记忆中枢，管理短期和长期记忆
  - Planner：任务规划器，生成执行计划
  - Tool Caller：工具调用器，执行外部工具
  - Reflector：反思优化器，评估和优化策略
  - 使用MCP协议进行模块间通信

- **RAG模块** (`modules/rag/`)：知识库检索增强生成
  - 心理健康专业知识库
  - 基于ChromaDB的语义检索

- **Intent模块** (`modules/intent/`)：混合式意图识别系统
  - 规则引擎（Rule Engine）：关键词快速匹配
  - ML分类器（ML Classifier）：语义意图识别
  - 支持6大意图类型：emotion、advice、conversation、function、crisis、chat

- **LLM模块** (`modules/llm/`)：大语言模型服务提供者
  - 支持多种LLM提供商（通义千问、OpenAI等）
  - 统一的LLM服务接口

- **Multimodal模块** (`modules/multimodal/`)：多模态处理
  - ASR：语音识别
  - TTS：语音合成
  - 图像理解和分析

### 核心目录结构

```
backend/
├── modules/                 # 核心模块（模块化架构）
│   ├── agent/              # Agent智能核心（使用MCP协议）
│   ├── rag/                # RAG知识库
│   ├── intent/             # 意图识别
│   ├── llm/                # LLM服务
│   └── multimodal/         # 多模态处理
├── routers/                # API路由层
├── services/               # 服务层（业务逻辑）
├── core/                   # 核心工具和配置
│   ├── config.py           # 配置管理
│   ├── interfaces.py       # 接口定义
│   ├── exceptions.py       # 异常定义
│   └── utils/              # 工具函数
├── middleware/             # 中间件
├── plugins/                # 插件系统
└── app.py                  # 应用工厂

frontend/
├── src/
│   ├── components/         # React组件
│   ├── pages/              # 页面
│   └── services/           # API服务
└── package.json

alembic/                    # 数据库迁移
├── versions/               # 迁移脚本
└── env.py                  # Alembic配置
```

## 配置说明

### 环境配置

复制配置模板并填写必需配置：

```bash
cp config.env.example config.env
```

**必需配置**：
- `LLM_API_KEY`：通义千问API密钥（也兼容 `DASHSCOPE_API_KEY` 或 `OPENAI_API_KEY`）
- `MYSQL_HOST`、`MYSQL_USER`、`MYSQL_PASSWORD`：MySQL数据库连接

**可选配置**：
- `LLM_BASE_URL`：LLM API基础URL（默认：https://api.openai.com/v1）
- `CHROMA_PERSIST_DIRECTORY`：ChromaDB持久化目录（默认：./chroma_db）
- `DEFAULT_MODEL`：默认模型名称（默认：gpt-4）
- `TEMPERATURE`：生成温度（默认：0.7）
- `MAX_TOKENS`：最大token数（默认：1000）

配置文件通过 `config.py` 加载，支持环境变量覆盖。

## Agent核心系统

Agent系统是情感聊天机器人的智能核心，包含以下核心组件：

### MCP协议通信

所有Agent模块间通信使用**MCP协议**（Model Context Protocol）：
- 标准化的消息格式
- 类型安全的消息传递
- 上下文管理和追踪
- 详见 `docs/MCP协议说明.md`

### Agent工作流程

1. **接收用户输入** → Memory Hub检索相关记忆
2. **Planner生成计划** → 确定需要调用的工具
3. **Tool Caller执行工具** → 搜索记忆、设置提醒等
4. **LLM生成回复** → 基于上下文和工具结果
5. **Reflector反思优化** → 评估交互质量，优化策略

### 可用工具

Agent支持以下工具（位于 `backend/modules/agent/core/agent/tools/`）：
- `search_memory`：搜索用户历史记忆
- `get_emotion_log`：获取情绪日志
- `set_reminder`：设置提醒
- `recommend_meditation`：推荐冥想音频
- `recommend_resource`：推荐心理健康资源
- `psychological_assessment`：心理健康评估
- `check_calendar`：查看日历事件

## 数据库管理

### Alembic迁移系统

项目使用**Alembic**管理数据库版本：

- 迁移脚本位于 `alembic/versions/`
- 迁移管理通过 `db_manager.py` 脚本和 `emotional-chat` CLI
- 首次安装时务必运行 `uv run emotional-chat db upgrade`

### 创建新迁移

```bash
# 自动生成迁移（基于模型变更）
alembic revision --autogenerate -m "描述变更内容"

# 手动创建迁移
alembic revision -m "描述变更内容"
```

## 开发规则

### 代码规范

1. **中文优先**：
   - 所有代码注释、文档、commit信息使用中文
   - Git提交信息使用中文描述
   - 不要在commit中出现"Claude Code"

2. **测试先行**：
   - 提交代码前必须通过测试
   - 运行相关测试脚本确保功能正常

3. **模块化开发**：
   - 新功能应作为独立模块添加到 `backend/modules/`
   - 遵循现有的分层架构：routers → services → modules → database
   - 模块间通信优先使用MCP协议

4. **配置管理**：
   - 敏感信息不得硬编码，必须通过环境变量配置
   - 新增配置项应在 `config.env.example` 中添加示例

### 文件命名和组织

- Python模块使用小写下划线命名：`agent_core.py`
- 测试文件以 `test_` 开头：`test_agent.py`
- 文档放在 `docs/` 目录
- 每个核心模块应包含 `__init__.py` 导出主要接口

## 故障排除

### 常见问题

1. **数据库连接失败**：
   - 检查 `config.env` 中的数据库配置
   - 运行 `uv run emotional-chat db check` 测试连接
   - 确保MySQL服务正在运行

2. **ChromaDB初始化失败**：
   - 检查 `CHROMA_PERSIST_DIRECTORY` 路径是否可写
   - 运行 `uv run emotional-chat rag init` 初始化知识库

3. **LLM API调用失败**：
   - 验证 `LLM_API_KEY` 是否正确
   - 检查 `LLM_BASE_URL` 是否可访问
   - 查看后端日志了解详细错误

4. **前端无法连接后端**：
   - 确保后端服务在 8000 端口运行
   - 检查CORS配置（`backend/app.py`）
   - 查看浏览器控制台和网络请求

5. **Agent工具调用失败**：
   - 检查工具参数是否正确
   - 查看 `backend/modules/agent/core/agent/tools/` 工具实现
   - 运行 `python test_agent_tools.py` 测试工具

## 参考文档

详细文档位于 `docs/` 目录：

- **核心功能**：
  - `核心功能详解.md`：所有核心功能说明
  - `Agent核心模块实现总结.md`：Agent系统详细说明
  - `意图识别模块说明.md`：意图识别系统
  - `RAG实施步骤.md`：知识库实施指南
  - `MCP协议说明.md`：MCP协议详细说明

- **架构设计**：
  - `项目结构说明.md`：详细的目录结构和架构
  - `记忆系统架构.md`：记忆系统设计
  - `技术栈详解.md`：技术选型说明

- **开发指南**：
  - `安装指南.md`：详细安装步骤
  - `API接口文档.md`：API接口说明
  - `生产部署指南.md`：Docker和云服务器部署
