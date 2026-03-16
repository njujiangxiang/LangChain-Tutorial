"""
示例：Ollama 高级使用 - 生产级应用与优化

演示 Ollama 在生产环境中的高级应用、性能优化和最佳实践
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Callable
from dotenv import load_dotenv
import os
import time
import hashlib
import json
from pathlib import Path

load_dotenv()


# ==================== 高级缓存策略 ====================

def setup_sqlite_cache():
    """设置 SQLite 缓存"""
    print("=" * 60)
    print("SQLite 缓存设置")
    print("=" * 60)
    
    cache_path = "./.langchain_cache.db"
    set_llm_cache(SQLiteCache(database_path=cache_path))
    
    print(f"缓存路径：{cache_path}")
    print("启用缓存后，相同的请求会直接返回缓存结果，加快速度并节省资源。")
    
    llm = ChatOllama(model="qwen3.5:9b")
    
    # 第一次调用 (未缓存)
    print("\n第一次调用 (未缓存):")
    start = time.time()
    response1 = llm.invoke([HumanMessage(content="1+1 等于几？")])
    elapsed1 = time.time() - start
    print(f"耗时：{elapsed1:.3f}s")
    print(f"响应：{response1.content}")
    
    # 第二次调用 (命中缓存)
    print("\n第二次调用 (缓存命中):")
    start = time.time()
    response2 = llm.invoke([HumanMessage(content="1+1 等于几？")])
    elapsed2 = time.time() - start
    print(f"耗时：{elapsed2:.3f}s")
    print(f"响应：{response2.content}")
    
    print(f"\n性能提升：{elapsed1/elapsed2:.1f}x" if elapsed2 > 0 else "")


# ==================== 自定义模型包装器 ====================

class OllamaModelWrapper:
    """Ollama 模型包装器 - 生产级封装"""
    
    def __init__(
        self,
        model: str = "qwen3.5:9b",
        temperature: float = 0.7,
        max_retries: int = 3,
        timeout: int = 60,
        cache_enabled: bool = True
    ):
        self.model_name = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.timeout = timeout
        self.cache_enabled = cache_enabled
        self.cache: Dict[str, str] = {}
        
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
        )
    
    def _get_cache_key(self, messages: List) -> str:
        """生成缓存键"""
        content = str([m.content for m in messages])
        return hashlib.md5(content.encode()).hexdigest()
    
    def invoke(self, messages: List, **kwargs) -> str:
        """带重试和缓存的调用"""
        cache_key = self._get_cache_key(messages)
        
        # 检查缓存
        if self.cache_enabled and cache_key in self.cache:
            return self.cache[cache_key]
        
        # 重试逻辑
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self.llm.invoke(messages, **kwargs)
                result = response.content
                
                # 写入缓存
                if self.cache_enabled:
                    self.cache[cache_key] = result
                
                return result
                
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        
        raise last_error
    
    def batch_invoke(self, batch_messages: List[List], max_concurrency: int = 5) -> List[str]:
        """批量调用"""
        results = []
        for messages in batch_messages:
            result = self.invoke(messages)
            results.append(result)
        return results
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "model": self.model_name,
            "cache_size": len(self.cache),
            "cache_enabled": self.cache_enabled,
        }


def wrapper_example():
    """模型包装器示例"""
    print("\n" + "=" * 60)
    print("生产级模型包装器")
    print("=" * 60)
    
    wrapper = OllamaModelWrapper(
        model="qwen3.5:9b",
        temperature=0.7,
        max_retries=3,
        cache_enabled=True
    )
    
    # 单次调用
    messages = [HumanMessage(content="Python 是什么？")]
    result = wrapper.invoke(messages)
    print(f"单次调用：{result[:100]}...")
    
    # 批量调用
    batch = [
        [HumanMessage(content="什么是 AI？")],
        [HumanMessage(content="什么是 ML？")],
        [HumanMessage(content="什么是 DL？")],
    ]
    
    print("\n批量调用:")
    results = wrapper.batch_invoke(batch)
    for i, result in enumerate(results):
        print(f"  {i+1}. {result[:50]}...")
    
    # 统计信息
    stats = wrapper.get_stats()
    print(f"\n统计：{json.dumps(stats, indent=2)}")


# ==================== 复杂链式工作流 ====================

def complex_chain_workflow():
    """复杂链式工作流"""
    print("\n" + "=" * 60)
    print("复杂链式工作流 - 文章生成器")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.7)
    
    # 步骤 1: 生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为'{topic}'生成一个包含引言、3 个主体段落、结论的文章大纲。"
    )
    
    # 步骤 2: 扩展每个段落
    expand_prompt = ChatPromptTemplate.from_template(
        "根据以下大纲扩展成完整段落 (200 字左右):\n{outline}"
    )
    
    # 步骤 3: 润色
    polish_prompt = ChatPromptTemplate.from_template(
        "润色以下文本，使其更流畅、专业:\n{text}"
    )
    
    # 创建链
    outline_chain = outline_prompt | llm | StrOutputParser()
    expand_chain = expand_prompt | llm | StrOutputParser()
    polish_chain = polish_prompt | llm | StrOutputParser()
    
    # 完整工作流
    topic = "人工智能的发展"
    print(f"主题：{topic}\n")
    
    # 生成大纲
    print("步骤 1: 生成大纲")
    outline = outline_chain.invoke({"topic": topic})
    print(outline[:200] + "...\n")
    
    # 扩展
    print("步骤 2: 扩展段落")
    expanded = expand_chain.invoke({"outline": outline})
    print(expanded[:200] + "...\n")
    
    # 润色
    print("步骤 3: 润色")
    final = polish_chain.invoke({"text": expanded})
    print(final[:200] + "...\n")
    
    print(f"最终长度：{len(final)} 字符")


# ==================== 结构化数据提取 ====================

class EntityExtraction(BaseModel):
    """实体提取结果"""
    persons: List[str] = Field(description="人名列表")
    organizations: List[str] = Field(description="组织/公司名列表")
    locations: List[str] = Field(description="地点列表")
    dates: List[str] = Field(description="日期列表")
    summary: str = Field(description="一句话摘要")


def entity_extraction():
    """实体提取"""
    print("\n" + "=" * 60)
    print("结构化数据提取 - 命名实体识别")
    print("=" * 60)
    
    llm = ChatOllama(model="qwen3.5:9b", temperature=0.3)
    parser = JsonOutputParser(pydantic_object=EntityExtraction)
    
    prompt = ChatPromptTemplate.from_template("""
    从以下文本中提取实体信息：
    
    {text}
    
    {format_instructions}
    """)
    
    chain = prompt | llm | parser
    
    text = """
    2024 年 3 月 15 日，阿里巴巴集团 CEO 吴泳铭在杭州总部宣布，
    公司将投资 100 亿元用于人工智能研发。
    该项目将在北京、上海、深圳三地设立研发中心，
    预计招聘 5000 名工程师。
    """
    
    print(f"输入文本：{text[:100]}...\n")
    
    result = chain.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    
    print("提取结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")


# ==================== 对话管理系统 ====================

class ConversationManager:
    """对话管理器 - 带记忆和上下文"""
    
    def __init__(self, model: str = "qwen3.5:9b"):
        self.llm = ChatOllama(model=model, temperature=0.7)
        self.history: List = []
        self.system_prompt = "你是一个有帮助的助手。"
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示"""
        self.system_prompt = prompt
    
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        if role == "user":
            self.history.append(HumanMessage(content=content))
        elif role == "assistant":
            self.history.append(AIMessage(content=content))
    
    def invoke(self, user_input: str) -> str:
        """调用对话"""
        self.add_message("user", user_input)
        
        messages = [SystemMessage(content=self.system_prompt)] + self.history
        
        response = self.llm.invoke(messages)
        
        self.add_message("assistant", response.content)
        
        return response.content
    
    def get_history(self) -> List[Dict]:
        """获取对话历史"""
        return [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", 
             "content": m.content}
            for m in self.history
        ]
    
    def clear_history(self):
        """清空历史"""
        self.history = []
    
    def save_to_file(self, filepath: str):
        """保存对话到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.get_history(), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """从文件加载对话"""
        with open(filepath, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        self.history = []
        for msg in history:
            if msg["role"] == "user":
                self.history.append(HumanMessage(content=msg["content"]))
            else:
                self.history.append(AIMessage(content=msg["content"]))


def conversation_manager_example():
    """对话管理器示例"""
    print("\n" + "=" * 60)
    print("对话管理系统")
    print("=" * 60)
    
    manager = ConversationManager(model="qwen3.5:9b")
    manager.set_system_prompt("你是一个专业的旅行顾问。")
    
    # 多轮对话
    print("对话开始:\n")
    
    responses = []
    questions = [
        "我想去日本旅游，有什么建议？",
        "最佳季节是什么时候？",
        "预算大概需要多少？",
    ]
    
    for q in questions:
        print(f"用户：{q}")
        response = manager.invoke(q)
        print(f"助手：{response[:100]}...\n")
        responses.append(response)
    
    # 查看历史
    history = manager.get_history()
    print(f"对话轮数：{len(history) // 2}")
    
    # 保存到文件
    manager.save_to_file("./conversation_history.json")
    print("对话已保存到 conversation_history.json")


# ==================== 性能基准测试 ====================

def performance_benchmark():
    """性能基准测试"""
    print("\n" + "=" * 60)
    print("性能基准测试")
    print("=" * 60)
    
    models = [
        "qwen3.5:9b",
        "llama3:8b",
    ]
    
    test_prompt = "请用 100 字左右介绍 Python 编程语言。"
    messages = [HumanMessage(content=test_prompt)]
    
    print(f"测试问题：{test_prompt}\n")
    
    results = []
    
    for model_name in models:
        try:
            llm = ChatOllama(model=model_name)
            
            # 预热
            llm.invoke(messages)
            
            # 测试 3 次取平均
            times = []
            for _ in range(3):
                start = time.time()
                response = llm.invoke(messages)
                elapsed = time.time() - start
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            tokens_per_sec = len(response.content) / avg_time
            
            results.append({
                "model": model_name,
                "avg_time": avg_time,
                "chars_per_sec": tokens_per_sec,
            })
            
            print(f"{model_name}:")
            print(f"  平均耗时：{avg_time:.2f}s")
            print(f"  生成速度：{tokens_per_sec:.1f} 字符/秒\n")
            
        except Exception as e:
            print(f"{model_name}: 不可用 - {e}\n")


if __name__ == "__main__":
    print("\n🦙 Ollama 高级示例 - 生产级应用与优化\n")
    
    setup_sqlite_cache()
    wrapper_example()
    complex_chain_workflow()
    entity_extraction()
    conversation_manager_example()
    performance_benchmark()
    
    print("\n✅ Ollama 高级示例完成！")
    print("\n💡 提示：生产环境请根据实际情况调整参数和配置。")
