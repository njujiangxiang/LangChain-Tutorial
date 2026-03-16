"""
示例：阿里云百炼中级使用 - 高级特性与优化

演示阿里云百炼的高级功能、性能优化和实用技巧
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import time
from typing import List, Dict, Optional

load_dotenv()


def get_aliyun_llm(model: str = "qwen-plus", **kwargs):
    """获取阿里云 LLM 实例"""
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY 未配置")
    
    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs
    )


def model_selection_guide():
    """模型选择指南"""
    print("=" * 60)
    print("阿里云模型选择指南")
    print("=" * 60)
    
    print("""
    阿里云百炼提供多种模型，根据场景选择:
    
    1. qwen-turbo
       - 特点：速度最快，成本最低
       - 适用：简单问答、文本分类、高并发场景
       - 成本：￥0.002/1K tokens
    
    2. qwen-plus
       - 特点：性能平衡，性价比高
       - 适用：大多数通用任务、内容创作
       - 成本：￥0.004/1K tokens
    
    3. qwen-max
       - 特点：最强性能，处理复杂推理
       - 适用：复杂分析、专业领域、代码生成
       - 成本：￥0.02/1K tokens
    
    4. qwen-vl-max
       - 特点：多模态，支持图像理解
       - 适用：图像问答、视觉分析、OCR
       - 成本：按调用计费
    """)


def advanced_parameters():
    """高级参数配置"""
    print("\n" + "=" * 60)
    print("高级参数配置")
    print("=" * 60)
    
    llm = get_aliyun_llm(
        model="qwen-plus",
        temperature=0.7,
        max_tokens=1024,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )
    
    print(f"模型：qwen-plus")
    print(f"参数配置:")
    print(f"  - temperature: 0.7 (创造性)")
    print(f"  - max_tokens: 1024 (最大生成长度)")
    print(f"  - top_p: 0.9 (核采样)")
    print(f"  - frequency_penalty: 0.5 (频率惩罚)")
    print(f"  - presence_penalty: 0.5 (存在惩罚)")
    
    # 测试
    messages = [HumanMessage(content="你好，请自我介绍")]
    response = llm.invoke(messages)
    print(f"\n响应：{response.content[:100]}...")


def streaming_response():
    """流式响应"""
    print("\n" + "=" * 60)
    print("流式响应")
    print("=" * 60)
    
    llm = get_aliyun_llm(model="qwen-plus", streaming=True)
    
    messages = [
        HumanMessage(content="请写一段 200 字左右的自我介绍。")
    ]
    
    print("流式输出：")
    print("-" * 60)
    
    full_response = ""
    for chunk in llm.stream(messages):
        content = chunk.content
        print(content, end="", flush=True)
        full_response += content
    
    print("\n" + "-" * 60)
    print(f"总长度：{len(full_response)} 字符")


def multi_turn_conversation():
    """多轮对话"""
    print("\n" + "=" * 60)
    print("多轮对话")
    print("=" * 60)
    
    llm = get_aliyun_llm(model="qwen-plus", temperature=0.7)
    
    # 系统提示
    system_prompt = """你是一个专业的客服助手。
    要求：
    1. 友好、专业
    2. 记住用户的历史信息
    3. 回答简洁明了
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="我想买一台笔记本电脑，预算 5000 元左右。"),
        AIMessage(content="好的，5000 元预算可以买到不错的笔记本了。请问您主要用途是什么？比如办公、游戏、还是设计？"),
        HumanMessage(content="主要是办公用，偶尔看看视频。"),
    ]
    
    response = llm.invoke(messages)
    print(f"用户：主要是办公用，偶尔看看视频。")
    print(f"客服：{response.content}")


def structured_output_with_pydantic():
    """使用 Pydantic 的结构化输出"""
    print("\n" + "=" * 60)
    print("结构化输出 (Pydantic)")
    print("=" * 60)
    
    # 定义输出格式
    class ProductReview(BaseModel):
        sentiment: str = Field(description="情感倾向：positive/negative/neutral")
        rating: int = Field(description="评分 1-5")
        keywords: List[str] = Field(description="关键词列表")
        summary: str = Field(description="一句话总结")
        pros: List[str] = Field(description="优点列表")
        cons: List[str] = Field(description="缺点列表")
    
    llm = get_aliyun_llm(model="qwen-plus", temperature=0.3)
    
    # 使用 JsonOutputParser
    parser = JsonOutputParser(pydantic_object=ProductReview)
    
    prompt = ChatPromptTemplate.from_template("""
    分析以下产品评论并提取结构化信息：
    
    评论：{review}
    
    {format_instructions}
    """)
    
    chain = prompt | llm | parser
    
    review = """
    这款笔记本电脑真的很不错！性能强劲，外观时尚，屏幕显示效果很棒。
    电池续航也很好，基本能用一整天。
    唯一的问题是风扇声音有点大，而且价格稍贵。
    总体来说很满意，推荐购买！
    """
    
    print(f"分析评论：{review[:100]}...\n")
    
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })
    
    print("结构化结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")


def prompt_optimization():
    """提示优化技巧"""
    print("\n" + "=" * 60)
    print("提示优化技巧")
    print("=" * 60)
    
    llm = get_aliyun_llm(model="qwen-plus", temperature=0.5)
    
    # 技巧 1: 提供示例 (Few-shot)
    few_shot_prompt = ChatPromptTemplate.from_template("""
    根据示例，完成类似任务：
    
    示例 1:
    输入：这个电影太棒了！
    输出：正面
    
    示例 2:
    输入：完全浪费钱，不好看。
    输出：负面
    
    示例 3:
    输入：还行吧，没什么特别的。
    输出：中性
    
    现在请分析：
    输入：{text}
    输出：""")
    
    chain = few_shot_prompt | llm | StrOutputParser()
    
    test_texts = [
        "产品质量很好，物流也快！",
        "客服态度太差了，再也不会买了。",
        "一般般，符合这个价位的水平。"
    ]
    
    print("Few-shot 情感分析:")
    for text in test_texts:
        result = chain.invoke({"text": text})
        print(f"  '{text[:20]}...' -> {result.strip()}")


def error_handling_best_practices():
    """错误处理最佳实践"""
    print("\n" + "=" * 60)
    print("错误处理最佳实践")
    print("=" * 60)
    
    def safe_invoke(messages, max_retries=3):
        """安全的 API 调用"""
        for attempt in range(max_retries):
            try:
                llm = get_aliyun_llm(model="qwen-plus")
                response = llm.invoke(messages)
                return response
            except Exception as e:
                error_msg = str(e)
                
                # 判断错误类型
                if "rate limit" in error_msg.lower():
                    print(f"  限流，等待 {2 ** attempt}秒...")
                    time.sleep(2 ** attempt)
                elif "authentication" in error_msg.lower():
                    print(f"  认证失败，检查 API Key")
                    raise
                elif attempt < max_retries - 1:
                    print(f"  重试 {attempt + 1}/{max_retries}: {error_msg}")
                    time.sleep(1)
                else:
                    print(f"  最大重试次数已用尽")
                    raise
        
        return None
    
    messages = [HumanMessage(content="测试")]
    
    try:
        response = safe_invoke(messages)
        print(f"调用成功：{response.content[:50]}...")
    except Exception as e:
        print(f"调用失败：{e}")


def cost_optimization():
    """成本优化技巧"""
    print("\n" + "=" * 60)
    print("成本优化技巧")
    print("=" * 60)
    
    print("""
    💡 降低成本的方法:
    
    1. 选择合适的模型
       - 简单任务用 qwen-turbo
       - 复杂任务用 qwen-max
       - 大多数用 qwen-plus
    
    2. 控制 token 使用
       - 设置 max_tokens 限制
       - 精简 prompt
       - 避免过长的上下文
    
    3. 使用缓存
       - 缓存常见问题的答案
       - 缓存 embedding 结果
    
    4. 批量处理
       - 合并多个请求
       - 减少 API 调用次数
    
    5. 监控用量
       - 设置预算告警
       - 定期审查使用情况
    """)


if __name__ == "__main__":
    print("\n☁️ 阿里云百炼中级示例 - 高级特性与优化\n")
    
    # 检查 API Key
    if not os.getenv('DASHSCOPE_API_KEY'):
        print("⚠️  DASHSCOPE_API_KEY 未配置")
        print("请在 .env 文件中添加：DASHSCOPE_API_KEY=your_key")
        print("\n显示示例代码结构...\n")
    
    try:
        model_selection_guide()
        advanced_parameters()
        streaming_response()
        multi_turn_conversation()
        structured_output_with_pydantic()
        prompt_optimization()
        error_handling_best_practices()
        cost_optimization()
        
        print("\n✅ 阿里云中级示例完成！")
    except Exception as e:
        print(f"\n⚠️  部分示例需要 API Key: {e}")
        print("配置后可运行完整示例。")
