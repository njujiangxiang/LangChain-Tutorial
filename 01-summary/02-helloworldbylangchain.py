"""
Hello World - 使用 LangChain 调用阿里云百炼 API
配置方式：
    1. 复制 .env.example 为 .env
    2. 在 .env 中配置 ALIYUN_API_KEY
    3. 可选：修改 config.yaml 调整其他配置
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI

# 加载环境变量
load_dotenv()

# 从环境变量或默认值配置
api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
model_name = os.getenv("DEFAULT_MODEL", "qwen3.5-plus")


local_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
local_model_name = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")

# 初始化模型 对话模式
model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
)


# 初始化模型 非对话模式
model_nochat = ChatOpenAI(
    model=local_model_name,
    api_key=api_key,
    base_url=local_base_url,
    max_tokens=500,
)


# 定义调用模型的函数 对话模式  模型直接回复
def ask(question: str) -> str:
    """调用模型并返回回复"""
    response = model.invoke(question)
    return response.content

# 定义调用模型的函数 非对话模式  模型流式回复
def ask_stream(question: str) -> str:
    """流式调用模型并打印回复"""
    full_response = ""
    for chunk in model.stream(question):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    print()
    return full_response


if __name__ == "__main__":
    print("Hello, World!")
    print(f"使用模型：{model_name}\n")

    print("普通调用:")
    result = ask("您好，您是谁？")
    print(result)

    print("\n非对话模式调用 (Ollama):")
    result = model_nochat.invoke("我姓江名翔，帮我儿子起一个名字")
    print(result.content)
