"""
Hello World - 使用原生 OpenAI SDK 调用阿里云百炼 API
注意：此示例使用硬编码的 API Key，生产环境请使用环境变量
"""

from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼 API Key 替换：api_key="sk-xxx"
    api_key="sk-ea696c7fcc5a44efb003c7876cb02bc1",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


print("Hello, World!")
# model: qwen3.5-plus
# api_key :sk-cc52517c86af46229520c677a78a1739

# 构建聊天消息
messages = [{"role": "user", "content": "今天南京的天气？"}]

# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-flash-2026-02-23",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": False, "enable_search": True},  # 启用搜索功能
    stream=True  # 启用流式输出
)

is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)

# 流式处理响应
for chunk in completion:
    delta = chunk.choices[0].delta
    
    # 输出思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    
    # 输出回复内容
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)