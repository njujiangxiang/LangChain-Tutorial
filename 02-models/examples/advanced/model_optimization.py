"""
示例：模型性能优化

演示如何优化模型调用的性能、成本和可靠性
"""

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
import os
import time
from functools import wraps
import hashlib
import json

# 加载环境变量
load_dotenv()


# ============================================================
# 1. 缓存装饰器
# ============================================================

class ResponseCache:
    """简单的内存缓存"""
    
    def __init__(self):
        self.cache = {}
    
    def _make_key(self, model_name: str, messages: list) -> str:
        """生成缓存键"""
        content = f"{model_name}:{json.dumps(messages, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, model_name: str, messages: list):
        """获取缓存"""
        key = self._make_key(model_name, messages)
        return self.cache.get(key)
    
    def set(self, model_name: str, messages: list, response: str):
        """设置缓存"""
        key = self._make_key(model_name, messages)
        self.cache[key] = response
    
    def stats(self):
        """返回缓存统计"""
        return {"size": len(self.cache)}


# 全局缓存实例
cache = ResponseCache()


def cached_call(ttl_seconds: int = 3600):
    """
    缓存装饰器
    
    Args:
        ttl_seconds: 缓存有效期 (秒)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(messages, **kwargs):
            # 尝试从缓存获取
            cached = cache.get(func.__name__, messages)
            if cached:
                print("  ⚡ 从缓存获取")
                return cached
            
            # 调用实际函数
            print("  🔄 调用模型...")
            result = func(messages, **kwargs)
            
            # 存入缓存
            cache.set(func.__name__, messages, result)
            return result
        
        return wrapper
    return decorator


# ============================================================
# 2. 重试机制
# ============================================================

def retry_call(max_retries: int = 3, delay: float = 1.0):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔 (秒)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        print(f"  🔄 重试 {attempt}/{max_retries}")
                        time.sleep(delay)
                    
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    print(f"  ❌ 尝试 {attempt + 1} 失败：{e}")
            
            raise last_exception
        
        return wrapper
    return decorator


# ============================================================
# 3. 性能监控
# ============================================================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.stats = {
            'total_calls': 0,
            'total_time': 0,
            'total_tokens': 0,
            'cache_hits': 0,
        }
    
    def record_call(self, duration: float, tokens: int = 0, cache_hit: bool = False):
        """记录一次调用"""
        self.stats['total_calls'] += 1
        self.stats['total_time'] += duration
        self.stats['total_tokens'] += tokens
        if cache_hit:
            self.stats['cache_hits'] += 1
    
    def summary(self):
        """返回性能摘要"""
        avg_time = self.stats['total_time'] / max(self.stats['total_calls'], 1)
        cache_rate = self.stats['cache_hits'] / max(self.stats['total_calls'], 1) * 100
        
        return {
            '总调用次数': self.stats['total_calls'],
            '总耗时': f"{self.stats['total_time']:.2f}s",
            '平均耗时': f"{avg_time:.2f}s",
            '总 token 数': self.stats['total_tokens'],
            '缓存命中率': f"{cache_rate:.1f}%"
        }


# 全局监控器
monitor = PerformanceMonitor()


def monitored_call(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        duration = time.time() - start_time
        # 估算 token 数 (简单估算)
        tokens = len(str(result)) // 4
        
        monitor.record_call(duration, tokens)
        
        print(f"  ⏱️  耗时：{duration:.2f}s")
        
        return result
    
    return wrapper


# ============================================================
# 4. 优化示例
# ============================================================

@monitored_call
@cached_call()
@retry_call(max_retries=2)
def optimized_llm_call(messages, model_name: str = 'ollama'):
    """
    优化的 LLM 调用
    
    包含：缓存、重试、监控
    """
    if model_name == 'ollama':
        llm = ChatOllama(model="qwen3.5:9b")
    elif model_name == 'anthropic' and os.getenv('ANTHROPIC_API_KEY'):
        llm = ChatAnthropic(model="claude-3-sonnet-20240229")
    elif model_name == 'openai' and os.getenv('OPENAI_API_KEY'):
        llm = ChatOpenAI(model="gpt-3.5-turbo")
    else:
        llm = ChatOllama(model="qwen3.5:9b")
    
    response = llm.invoke(messages)
    return response.content


def test_caching():
    """测试缓存功能"""
    print("=" * 60)
    print("缓存优化")
    print("=" * 60)
    
    from langchain_core.messages import HumanMessage
    
    question = "什么是人工智能？"
    messages = [HumanMessage(content=question)]
    
    print("\n第一次调用 (实际调用):")
    result1 = optimized_llm_call(messages, model_name='ollama')
    print(f"结果：{result1[:100]}...")
    
    print("\n第二次调用 (应该命中缓存):")
    result2 = optimized_llm_call(messages, model_name='ollama')
    print(f"结果：{result2[:100]}...")
    
    print(f"\n缓存统计：{cache.stats()}")


def test_retry_mechanism():
    """测试重试机制"""
    print("\n" + "=" * 60)
    print("重试机制")
    print("=" * 60)
    
    # 创建一个会失败的调用
    @retry_call(max_retries=3, delay=0.5)
    def flaky_call():
        import random
        if random.random() < 0.7:  # 70% 失败率
            raise Exception("模拟网络错误")
        return "成功!"
    
    print("测试不稳定的调用 (70% 失败率):")
    try:
        result = flaky_call()
        print(f"最终结果：{result}")
    except Exception as e:
        print(f"所有重试失败：{e}")


def test_performance_monitoring():
    """测试性能监控"""
    print("\n" + "=" * 60)
    print("性能监控")
    print("=" * 60)
    
    from langchain_core.messages import HumanMessage
    
    questions = [
        "1+1=?",
        "地球形状？",
        "Python 是什么？"
    ]
    
    print("\n执行多次调用并监控性能:\n")
    
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
        messages = [HumanMessage(content=q)]
        result = optimized_llm_call(messages, model_name='ollama')
        print(f"   {result[:50]}...\n")
    
    # 打印性能摘要
    print("📊 性能摘要:")
    stats = monitor.summary()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def test_batch_optimization():
    """测试批量优化"""
    print("\n" + "=" * 60)
    print("批量处理优化")
    print("=" * 60)
    
    from langchain_core.messages import HumanMessage
    
    # 批量问题
    questions = [
        f"问题{i}" for i in range(5)
    ]
    
    print("\n串行处理 (简单但慢):")
    start = time.time()
    for q in questions:
        messages = [HumanMessage(content=q)]
        optimized_llm_call(messages, model_name='ollama')
    serial_time = time.time() - start
    print(f"总耗时：{serial_time:.2f}s")
    
    # 注意：LangChain 本身不支持真正的并行调用
    # 实际应用中可以使用 asyncio 或 concurrent.futures


def test_token_optimization():
    """测试 token 优化"""
    print("\n" + "=" * 60)
    print("Token 优化技巧")
    print("=" * 60)
    
    print("""
    💡 Token 优化建议:
    
    1. 精简提示词:
       ❌ "请你作为一个经验丰富的 Python 程序员，帮我解释一下..."
       ✅ "解释：什么是列表推导式？"
    
    2. 限制输出长度:
       - 使用 max_tokens 参数
       - 在提示中明确要求"简短回答"
    
    3. 减少上下文:
       - 只保留必要的对话历史
       - 使用摘要代替完整历史
    
    4. 结构化输出:
       - 使用 JSON 等紧凑格式
       - 避免冗余的格式和说明
    
    5. 缓存重复查询:
       - 相同问题直接返回缓存
       - 相似问题使用语义缓存
    """)


if __name__ == "__main__":
    print("\n⚡ 模型性能优化示例\n")
    
    test_caching()
    test_retry_mechanism()
    test_performance_monitoring()
    test_batch_optimization()
    test_token_optimization()
    
    print("\n✅ 所有测试完成！")
