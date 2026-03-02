from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key="sk-ea696c7fcc5a44efb003c7876cb02bc1",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


print("Hello, World!")
# model: qwen3.5-plus
# api_key :sk-cc52517c86af46229520c677a78a1739

messages = [{"role": "user", "content": "今天南京的天气？"}]
completion = client.chat.completions.create(
    model="qwen3.5-flash-2026-02-23",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": False ,"enable_search": True},
    stream=True
)
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in completion:
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)