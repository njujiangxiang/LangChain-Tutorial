"""
Hello World - 使用原生 OpenAI SDK 调用阿里云百炼 API
配置方式：
    1. 复制 .env.example 为 .env
    2. 在 .env 中配置 ALIYUN_API_KEY
    3. 可选：修改 config.yaml 调整其他配置
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 加载配置文件（从项目根目录加载）
root_path = Path(__file__).parent.parent
config_path = root_path / "config.yaml"

api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
model_name = os.getenv("DEFAULT_MODEL", "qwen3.5-plus")

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def chat(messages: list, enable_thinking: bool = True, stream: bool = True):
    """发送聊天请求并流式输出结果"""
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        extra_body={"enable_thinking": enable_thinking} if enable_thinking else None,
        stream=stream,
    )

    is_answering = False
    separator = "=" * 20

    if enable_thinking:
        print(f"\n{separator}思考过程{separator}\n")

    for chunk in completion:
        delta = chunk.choices[0].delta

        # 输出思考内容
        if enable_thinking and hasattr(delta, "reasoning_content") and delta.reasoning_content:
            print(delta.reasoning_content, end="", flush=True)

        # 输出回复内容
        if hasattr(delta, "content") and delta.content:
            if not is_answering and enable_thinking:
                print(f"\n{separator}完整回复{separator}\n")
                is_answering = True
            print(delta.content, end="", flush=True)

    print()  # 换行


if __name__ == "__main__":
    print("Hello, World!")
    print(f"使用模型：{model_name}\n")

    messages = [{"role": "user", "content": "你是谁"}]
    chat(messages)
