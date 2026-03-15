# 00-Setup - 环境配置

> 工欲善其事，必先利其器。配置好开发环境是学习 LangChain 的第一步！

---

## 🎯 学习目标

- ✅ 安装 Python 3.10+ 环境
- ✅ 创建虚拟环境
- ✅ 安装 LangChain 及相关依赖
- ✅ 配置 API 密钥
- ✅ 验证安装成功

---

## 📦 环境要求

### 系统要求
- Python 3.10 或更高版本
- pip 包管理器
- Git (用于克隆项目)

### API 密钥 (至少需要一个)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Anthropic API Key](https://console.anthropic.com/)
- [其他模型 API](../resources/api-links.md)

---

## 🚀 快速开始

### 1. 检查 Python 版本

```bash
python --version
# 应该显示 Python 3.10.x 或更高
```

### 2. 创建虚拟环境

```bash
# 在项目根目录
python -m venv .venv

# 激活虚拟环境
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装 LangChain 核心包
pip install langchain langchain-core langchain-community

# 安装常用集成
pip install langchain-openai langchain-anthropic

# 安装向量数据库
pip install faiss-cpu chromadb

# 安装文档处理
pip install pypdf python-docx beautifulsoup4

# 或者一次性安装所有依赖
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# macOS/Linux
nano .env  # 或用你喜欢的编辑器

# Windows
notepad .env
```

### 5. 验证安装

```bash
python examples/verify_install.py
```

---

## 📁 项目结构

```
LangChain-Tutorial/
├── .venv/                 # 虚拟环境
├── .env                   # 环境变量 (自己创建)
├── .env.example           # 环境变量模板
├── requirements.txt       # Python 依赖
├── 00-setup/              # 本目录
│   ├── README.md          # 本文件
│   ├── examples/          # 示例代码
│   │   └── verify_install.py
│   └── exercises/         # 练习
│       └── setup_check.py
└── ...
```

---

## 🔧 常见问题

### 问题 1: pip 安装慢

**解决方案**: 使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: 权限错误

**解决方案**: 使用虚拟环境或 --user 标志
```bash
pip install --user langchain
```

### 问题 3: 依赖冲突

**解决方案**: 创建新的虚拟环境
```bash
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📝 环境检查清单

- [ ] Python 3.10+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] LangChain 核心包已安装
- [ ] 至少一个模型 API 密钥已配置
- [ ] 验证脚本运行成功
- [ ] IDE/编辑器已配置 (可选)

---

## 🎓 下一步

完成环境配置后，继续学习：

1. [01-core-concepts](../01-core-concepts/README.md) - 核心概念
2. [02-models](../02-models/README.md) - 模型集成
3. [03-prompts](../03-prompts/README.md) - 提示工程

---

## 💡 提示

- 建议为每个项目创建独立的虚拟环境
- 使用 `.env` 文件管理敏感信息，不要提交到 Git
- 定期更新依赖包以获取最新功能和安全补丁

---

**配置完成后，运行验证脚本开始学习吧！** 🚀
