"""
Hello World - 使用原生 OpenAI SDK 调用阿里云百炼 API
配置方式：
    1. 复制 .env.example 为 .env
    2. 在 .env 中配置 ALIYUN_API_KEY
    3. 可选：修改 config.yaml 调整其他配置
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 加载配置文件（从项目根目录加载）
root_path = Path(__file__).parent.parent
config_path = root_path / "config.yaml"

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL", config['api']['base_url'])
model_name = os.getenv("DEFAULT_MODEL", config['api']['model'])
enable_thinking_default = config['api'].get('enable_thinking', True)
enable_search_default = config['api'].get('enable_search', False)

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def chat(messages: list, enable_thinking: bool = None, enable_search: bool = None, stream: bool = True):
    """发送聊天请求并流式输出结果

    Args:
        messages: 聊天消息列表
        enable_thinking: 是否启用思考过程输出（默认从配置文件读取）
        enable_search: 是否启用联网搜索功能（默认从配置文件读取）
        stream: 是否使用流式输出
    """
    # 使用配置文件默认值
    if enable_thinking is None:
        enable_thinking = enable_thinking_default
    if enable_search is None:
        enable_search = enable_search_default
    # 构建 extra_body 参数
    extra_body = {}
    if enable_thinking:
        extra_body["enable_thinking"] = True
    if enable_search:
        extra_body["enable_search"] = True

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        extra_body=extra_body if extra_body else None,
        stream=stream,
    )

    is_answering = False
    separator = "=" * 20

    if enable_thinking:
        print(f"\n{separator}思考过程{separator}\n")

    if enable_search:
        print(f"\n{separator}搜索内容{separator}\n")

    for chunk in completion:
        delta = chunk.choices[0].delta

        # 输出思考内容
        if enable_thinking and hasattr(delta, "reasoning_content") and delta.reasoning_content:
            print(delta.reasoning_content, end="", flush=True)

        # 输出搜索内容
        if enable_search and hasattr(delta, "search_info") and delta.search_info:
            print(delta.search_info, end="", flush=True)

        # 输出回复内容
        if hasattr(delta, "content") and delta.content:
            if not is_answering and (enable_thinking or enable_search):
                print(f"\n{separator}完整回复{separator}\n")
                is_answering = True
            print(delta.content, end="", flush=True)

    print()  # 换行


if __name__ == "__main__":
    print("Hello, World!")
    print(f"使用模型：{model_name}\n")

    messages = [{"role": "user", "content": "今天南京的天气?"}]
    chat(messages)

    # 使用联网搜索功能示例
    print("\n" + "=" * 50)
    print("启用联网搜索功能示例")
    print("=" * 50 + "\n")

    search_messages = [{"role": "user", "content": "今天有什么热点新闻？"}]
    chat(search_messages, enable_thinking=False, enable_search=True)
