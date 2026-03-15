"""
HTTP 服务 - 流式返回大模型结果
使用方法:
    python http_server.py
    然后访问 http://localhost:8000/chat?message=你好
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn

# 加载环境变量
load_dotenv()

# 加载配置文件
root_path = Path(__file__).parent.parent
config_path = root_path / "config.yaml"

api_key = os.getenv("ALIYUN_API_KEY")
base_url = os.getenv("ALIYUN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
model_name = os.getenv("DEFAULT_MODEL", "qwen3.5-flash")

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

# 初始化 FastAPI 应用
app = FastAPI(title="LangChain Chat API", description="流式聊天 API")


async def generate_response(message: str, enable_thinking: bool = True):
    """生成器：流式返回大模型响应"""
    messages = [{"role": "user", "content": message}]

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        extra_body={"enable_thinking": enable_thinking,"enable_search": True} if enable_thinking else None,
        stream=True,
    )

    is_answering = False
    separator = "=" * 20

    if enable_thinking:
        yield f"\n{separator}思考过程{separator}\n\n"

    for chunk in completion:
        delta = chunk.choices[0].delta

        # 输出思考内容
        if enable_thinking and hasattr(delta, "reasoning_content") and delta.reasoning_content:
            yield delta.reasoning_content

        # 输出回复内容
        if hasattr(delta, "content") and delta.content:
            if not is_answering and enable_thinking:
                yield f"\n{separator}完整回复{separator}\n\n"
                is_answering = True
            yield delta.content

    yield "\n"


@app.get("/chat")
async def chat(
    message: str,
    enable_thinking: bool = True,
):
    """
    聊天接口 - 流式返回大模型结果

    参数:
        message: 用户输入的消息
        enable_thinking: 是否启用思考过程 (默认 True)

    返回:
        流式文本响应
    """
    return StreamingResponse(
        generate_response(message, enable_thinking),
        media_type="text/plain",
    )


@app.get("/health")
async def health():
    """健康检查接口"""
    return {"status": "ok", "model": model_name}


if __name__ == "__main__":
    print(f"启动 HTTP 服务...")
    print(f"模型：{model_name}")
    print(f"地址：http://localhost:8000")
    print(f"接口：http://localhost:8000/chat?message=你好")

    uvicorn.run(app, host="0.0.0.0", port=8000)
