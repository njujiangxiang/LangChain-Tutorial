"""
示例：阿里云百炼高级使用 - 生产级应用与最佳实践

演示阿里云百炼在生产环境中的高级应用、性能优化和最佳实践
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os
import time
import hashlib
import json
from datetime import datetime

load_dotenv()


def get_aliyun_llm(model: str = "qwen-plus", **kwargs):
    """获取阿里云 LLM 实例"""
    api_key = os.getenv('DASHSCOPE_API_KEY')
    
    if not api_key:
        print("⚠️  DASHSCOPE_API_KEY 未配置，使用演示模式")
        return None
    
    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        **kwargs
    )


# ==================== 生产级缓存 ====================

def setup_production_cache():
    """生产级缓存设置"""
    print("=" * 60)
    print("生产级缓存策略")
    print("=" * 60)
    
    cache_path = "./.aliyun_cache.db"
    set_llm_cache(SQLiteCache(database_path=cache_path))
    
    print(f"缓存路径：{cache_path}")
    print("""
    缓存策略:
    1. SQLite 缓存：持久化缓存，重启后依然有效
    2. 适用场景：FAQ、常见问题、固定模板
    3. 注意事项：定期清理过期缓存
    """)


# ==================== 多模型路由 ====================

class ModelRouter:
    """多模型路由器 - 根据任务复杂度选择模型"""
    
    def __init__(self):
        self.models = {
            "simple": get_aliyun_llm(model="qwen-turbo", temperature=0.5),
            "standard": get_aliyun_llm(model="qwen-plus", temperature=0.7),
            "complex": get_aliyun_llm(model="qwen-max", temperature=0.8),
        }
    
    def classify_task(self, text: str) -> str:
        """简单分类任务复杂度"""
        word_count = len(text)
        
        if word_count < 20:
            return "simple"
        elif word_count < 100:
            return "standard"
        else:
            return "complex"
    
    def invoke(self, messages: List, task_type: str = None) -> str:
        """智能路由调用"""
        if task_type is None:
            # 自动分类
            text = messages[-1].content if messages else ""
            task_type = self.classify_task(text)
        
        llm = self.models.get(task_type, self.models["standard"])
        
        if llm is None:
            return "[演示模式] API Key 未配置"
        
        response = llm.invoke(messages)
        return response.content
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "simple": "qwen-turbo - 快速简单任务",
            "standard": "qwen-plus - 标准通用任务",
            "complex": "qwen-max - 复杂专业任务",
        }


def model_router_example():
    """模型路由器示例"""
    print("\n" + "=" * 60)
    print("多模型路由器")
    print("=" * 60)
    
    router = ModelRouter()
    
    print("模型路由策略:")
    for level, info in router.get_model_info().items():
        print(f"  {level}: {info}")
    
    # 测试不同复杂度任务
    test_cases = [
        ("1+1=?", "simple"),
        ("请介绍 Python 的主要特点和应用场景。", "standard"),
        ("请详细分析人工智能技术的发展历程、当前趋势、未来挑战，以及对各行业的影响。", "complex"),
    ]
    
    print("\n测试路由:")
    for text, expected_level in test_cases:
        classified = router.classify_task(text)
        print(f"  文本长度：{len(text)} -> 分类：{classified} (预期：{expected_level})")


# ==================== 复杂工作流 ====================

def advanced_rag_workflow():
    """高级 RAG 工作流示例"""
    print("\n" + "=" * 60)
    print("高级 RAG 工作流")
    print("=" * 60)
    
    llm = get_aliyun_llm(model="qwen-plus")
    
    if llm is None:
        print("演示代码:")
        print("""
        # RAG 工作流:
        1. 文档加载和分块
        2. 生成 embedding
        3. 向量检索
        4. 上下文增强生成
        
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import DashScopeEmbeddings
        
        embeddings = DashScopeEmbeddings(model="text-embedding-v1")
        vectorstore = FAISS.from_texts(documents, embeddings)
        retriever = vectorstore.as_retriever()
        """)
        return
    
    print("""
    RAG 工作流步骤:
    
    1. 文档处理
       - 加载文档 (PDF/Word/TXT)
       - 文本分块 (chunk_size=500)
       - 清理和预处理
    
    2. 向量化
       - 使用 text-embedding-v1 生成 embedding
       - 存储到向量数据库 (FAISS/Chroma)
    
    3. 检索
       - 相似度搜索 (top_k=5)
       - 重排序 (可选)
    
    4. 生成
       - 构建增强 prompt
       - LLM 生成答案
    """)


# ==================== 监控和日志 ====================

class LLMMonitor:
    """LLM 调用监控器"""
    
    def __init__(self):
        self.calls: List[Dict] = []
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def log_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency: float,
        success: bool
    ):
        """记录调用"""
        call_record = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_ms": int(latency * 1000),
            "success": success,
        }
        
        self.calls.append(call_record)
        self.total_tokens += input_tokens + output_tokens
        
        # 估算成本 (简化)
        cost_per_1k = 0.004  # qwen-plus 价格
        self.total_cost += (input_tokens + output_tokens) / 1000 * cost_per_1k
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.calls:
            return {"calls": 0}
        
        return {
            "total_calls": len(self.calls),
            "total_tokens": self.total_tokens,
            "estimated_cost": self.total_cost,
            "avg_latency_ms": sum(c["latency_ms"] for c in self.calls) / len(self.calls),
            "success_rate": sum(1 for c in self.calls if c["success"]) / len(self.calls),
        }
    
    def export_report(self, filepath: str):
        """导出报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "stats": self.get_stats(),
                "calls": self.calls,
            }, f, ensure_ascii=False, indent=2)


def monitor_example():
    """监控器示例"""
    print("\n" + "=" * 60)
    print("LLM 调用监控")
    print("=" * 60)
    
    monitor = LLMMonitor()
    
    # 模拟调用记录
    monitor.log_call("qwen-plus", 100, 200, 1.5, True)
    monitor.log_call("qwen-plus", 150, 250, 2.0, True)
    monitor.log_call("qwen-turbo", 80, 120, 0.8, True)
    monitor.log_call("qwen-max", 300, 500, 3.5, False)
    
    stats = monitor.get_stats()
    
    print("调用统计:")
    print(f"  总调用：{stats['total_calls']}")
    print(f"  总 tokens: {stats['total_tokens']}")
    print(f"  估算成本：￥{stats['estimated_cost']:.4f}")
    print(f"  平均延迟：{stats['avg_latency_ms']:.1f}ms")
    print(f"  成功率：{stats['success_rate']*100:.1f}%")
    
    # 导出报告
    monitor.export_report("./llm_usage_report.json")
    print("\n报告已导出到 llm_usage_report.json")


# ==================== 安全与审计 ====================

def security_best_practices():
    """安全最佳实践"""
    print("\n" + "=" * 60)
    print("安全与审计最佳实践")
    print("=" * 60)
    
    print("""
    🔐 安全建议:
    
    1. API Key 管理
       - 使用环境变量存储
       - 定期轮换密钥
       - 设置使用限额
       - 不同环境使用不同 Key
    
    2. 输入安全
       - 过滤敏感信息 (密码、身份证、银行卡)
       - 限制输入长度
       - 检测并阻止注入攻击
    
    3. 输出安全
       - 过滤不当内容
       - 验证输出格式
       - 避免泄露敏感信息
    
    4. 审计日志
       - 记录所有 API 调用
       - 保存输入输出
       - 定期审查异常
    
    5. 速率限制
       - 实现客户端限流
       - 避免触发 API 限流
       - 使用指数退避重试
    """)
    
    # 敏感信息过滤示例
    def filter_sensitive(text: str) -> str:
        """过滤敏感信息"""
        import re
        
        # 手机号
        text = re.sub(r'1[3-9]\\d{9}', '[PHONE]', text)
        # 身份证
        text = re.sub(r'\\d{17}[\\dXx]', '[ID_CARD]', text)
        # 邮箱
        text = re.sub(r'[\\w.-]+@[\\w.-]+', '[EMAIL]', text)
        
        return text
    
    test_text = "我的电话是 13812345678，邮箱是 test@example.com"
    filtered = filter_sensitive(test_text)
    print(f"\n过滤示例:")
    print(f"  原始：{test_text}")
    print(f"  过滤：{filtered}")


# ==================== 成本优化 ====================

def cost_optimization_strategies():
    """成本优化策略"""
    print("\n" + "=" * 60)
    print("成本优化策略")
    print("=" * 60)
    
    print("""
    💰 降低成本的方法:
    
    1. 模型选择优化
       - 简单任务用 qwen-turbo (￥0.002/1K)
       - 通用任务用 qwen-plus (￥0.004/1K)
       - 复杂任务用 qwen-max (￥0.02/1K)
    
    2. Token 优化
       - 精简 prompt，去除冗余
       - 设置合理的 max_tokens
       - 使用摘要减少上下文
    
    3. 缓存策略
       - 缓存常见问题答案
       - 缓存 embedding 结果
       - 实现语义缓存
    
    4. 批量处理
       - 合并多个请求
       - 减少 API 调用次数
    
    5. 监控告警
       - 设置预算上限
       - 用量告警
       - 异常检测
    """)
    
    # 成本对比示例
    print("\n成本对比示例 (每 1000 tokens):")
    models = [
        ("qwen-turbo", 0.002),
        ("qwen-plus", 0.004),
        ("qwen-max", 0.020),
    ]
    
    monthly_tokens = 1000000  # 100 万 tokens/月
    
    print(f"\n月用量：{monthly_tokens:,} tokens")
    for model, price_per_1k in models:
        monthly_cost = monthly_tokens / 1000 * price_per_1k
        print(f"  {model}: ￥{monthly_cost:.2f}/月")


if __name__ == "__main__":
    print("\n☁️ 阿里云百炼高级示例 - 生产级应用与最佳实践\n")
    
    setup_production_cache()
    model_router_example()
    advanced_rag_workflow()
    monitor_example()
    security_best_practices()
    cost_optimization_strategies()
    
    print("\n✅ 阿里云高级示例完成！")
    print("\n💡 提示：生产环境请根据实际需求调整配置。")
