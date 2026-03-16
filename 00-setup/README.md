# 00-Setup - 环境配置与基础

> 工欲善其事，必先利其器。完成环境配置，开始 LangChain 学习之旅！

---

## 🎯 学习目标

- ✅ 完成 Python 环境配置
- ✅ 安装 LangChain 及依赖
- ✅ 配置 API 密钥
- ✅ 安装 Ollama 本地模型
- ✅ 验证环境安装

---

## 📦 环境要求

### 系统要求
- **操作系统**: macOS / Linux / Windows
- **Python 版本**: 3.10+ (推荐 3.11)
- **内存**: 至少 8GB (推荐 16GB+)
- **磁盘**: 至少 10GB 可用空间

### 检查 Python 版本
```bash
python3 --version
# 应显示 Python 3.10.x 或更高
```

---

## 🔧 安装步骤

### 步骤 1: 创建虚拟环境 (推荐)

```bash
# 进入项目目录
cd /Users/xiaoyu/code/LangChain-Tutorial

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate

# Windows:
# .venv\Scripts\activate
```

### 步骤 2: 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装所有依赖
pip install -r requirements.txt
```

### 步骤 3: 验证安装

```bash
python examples/verify_install.py
```

**预期输出**:
```
✅ 核心依赖验证成功!
  - LangChain: 0.3.x
  - LangChain Ollama: 0.3.x
  - FAISS: 1.x.x
  - ChromaDB: 1.x.x
  - PyPDF: 6.x.x
  - Pydantic: 2.x.x

✅ 环境配置完成！
```

---

## 🦙 安装 Ollama (本地模型)

### macOS 安装

```bash
# 使用 Homebrew
brew install ollama

# 或下载安装包
# 访问 https://ollama.ai 下载 macOS 版本
```

### Linux 安装

```bash
# 一键安装
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows 安装

1. 访问 [https://ollama.ai](https://ollama.ai)
2. 下载 Windows 安装包
3. 运行安装程序

### 下载模型

```bash
# 下载推荐模型 (qwen3.5:9b)
ollama pull qwen3.5:9b

# 其他可选模型
ollama pull llama3:8b      # Meta Llama 3 (8B)
ollama pull mistral:7b    # Mistral (7B)
ollama pull codellama:7b  # Code Llama (代码专用)

# 查看已下载模型
ollama list
```

### 启动 Ollama 服务

```bash
# 后台启动
ollama serve

# 验证服务
curl http://localhost:11434/api/version
```

---

## 🔑 配置 API 密钥

### 复制环境变量模板

```bash
cp .env.example .env
```

### 编辑 .env 文件

```bash
# 阿里云百炼 API Key (可选)
# 获取地址：https://dashscope.console.aliyun.com/
DASHSCOPE_API_KEY=your_api_key_here

# OpenAI API Key (可选)
OPENAI_API_KEY=your_api_key_here

# Anthropic API Key (可选)
ANTHROPIC_API_KEY=your_api_key_here

# Ollama 配置 (本地，无需 API Key)
OLLAMA_HOST=localhost:11434
```

### ⚠️ 安全提示

- **不要**将 `.env` 文件提交到 Git
- 已添加到 `.gitignore`，请确认
- 定期轮换 API 密钥
- 设置使用限额

---

## 📁 项目结构

```
LangChain-Tutorial/
├── .env                  # 环境变量 (不提交)
├── .env.example          # 环境变量模板
├── .gitignore            # Git 忽略文件
├── requirements.txt      # Python 依赖
├── .venv/                # 虚拟环境 (不提交)
├── 00-setup/             # 环境配置
│   ├── README.md
│   ├── examples/
│   │   └── verify_install.py
│   └── exercises/
├── 01-core-concepts/     # 核心概念
├── 02-models/            # 模型集成
└── ...                   # 其他章节
```

---

## ✅ 验证安装

### 运行验证脚本

```bash
cd 00-setup
python examples/verify_install.py
```

### 手动验证

```python
# test_install.py
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# 测试 Ollama
llm = ChatOllama(model="qwen3.5:9b")
response = llm.invoke([HumanMessage(content="你好")])
print(f"Ollama 响应：{response.content}")

print("✅ 所有组件正常工作！")
```

---

## 🐛 常见问题

### Q1: pip 安装失败
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: Ollama 服务无法启动
```bash
# 检查端口占用
lsof -i :11434

# 重启 Ollama
brew services restart ollama
# 或
ollama serve
```

### Q3: 模型下载失败
```bash
# 检查网络连接
# 使用国内镜像站
# 或手动下载模型文件
```

### Q4: 导入错误
```bash
# 确保激活了虚拟环境
source .venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

---

## 📚 下一步

完成环境配置后，继续学习：

1. **[01-core-concepts](../01-core-concepts/README.md)** - LangChain 核心概念
2. **[02-models](../02-models/README.md)** - 模型集成与调用
3. **[03-prompts](../03-prompts/README.md)** - 提示工程

---

## 💡 提示

- ✅ 推荐使用 **Ollama 本地模型** 进行学习（免费、快速）
- ✅ 生产环境根据需要选择 **阿里云/OpenAI** 等云端模型
- ✅ 遇到问题先查看 `examples/` 目录中的示例代码
- ✅ 记录学习笔记到 `notes/` 目录

---

**环境配置完成！开始你的 LangChain 学习之旅吧！🚀**

如有问题，欢迎在 Issues 中提问。
