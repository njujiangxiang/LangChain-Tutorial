"""
示例：模型切换与路由

演示如何在不同模型之间切换和路由
"""

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


class ModelRouter:
    """模型路由器 - 根据条件选择不同模型"""
    
    def __init__(self):
        self.models = {}
        self._init_models()
    
    def _init_models(self):
        """初始化可用的模型"""
        # Ollama 本地模型 (总是可用)
        self.models['ollama'] = ChatOllama(
            model="qwen3.5:9b",
            temperature=0.7
        )
        
        # Anthropic (如果有 API Key)
        if os.getenv('ANTHROPIC_API_KEY'):
            self.models['anthropic'] = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.7
            )
        else:
            print("ℹ️  Anthropic API Key 未配置")
        
        # OpenAI (如果有 API Key)
        if os.getenv('OPENAI_API_KEY'):
            self.models['openai'] = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7
            )
        else:
            print("ℹ️  OpenAI API Key 未配置")
    
    def get_model(self, model_name: str = 'auto'):
        """
        获取模型
        
        Args:
            model_name: 模型名称或 'auto' 自动选择
        
        Returns:
            选中的模型实例
        """
        if model_name == 'auto':
            # 自动选择：优先云端模型，降级到本地
            if 'anthropic' in self.models:
                return self.models['anthropic']
            elif 'openai' in self.models:
                return self.models['openai']
            else:
                return self.models['ollama']
        
        if model_name not in self.models:
            raise ValueError(f"模型 {model_name} 不可用")
        
        return self.models[model_name]
    
    def route_by_complexity(self, task: str):
        """
        根据任务复杂度路由
        
        Args:
            task: 任务描述
        
        Returns:
            选中的模型实例
        """
        # 简单关键词
        simple_keywords = ['翻译', '总结', '问候', '你好', '谢谢']
        complex_keywords = ['分析', '推理', '设计', '优化', '复杂']
        
        # 判断复杂度
        is_complex = any(kw in task for kw in complex_keywords)
        is_simple = any(kw in task for kw in simple_keywords)
        
        if is_complex and ('anthropic' in self.models or 'openai' in self.models):
            print(f"🔍 检测到复杂任务，使用云端模型")
            return self.get_model('anthropic' if 'anthropic' in self.models else 'openai')
        else:
            print(f"📝 检测到简单任务，使用本地模型")
            return self.get_model('ollama')


def test_model_router():
    """测试模型路由器"""
    print("=" * 60)
    print("模型路由器测试")
    print("=" * 60)
    
    router = ModelRouter()
    
    # 测试自动选择
    print("\n1️⃣  自动选择模型:")
    model = router.get_model('auto')
    print(f"选中模型：{type(model).__name__}")
    
    # 测试手动指定
    print("\n2️⃣  手动指定模型:")
    if 'ollama' in router.models:
        model = router.get_model('ollama')
        print(f"选中模型：{type(model).__name__}")
    
    # 测试按复杂度路由
    print("\n3️⃣  按复杂度路由:")
    simple_task = "你好，请问候我"
    complex_task = "请分析这个复杂的技术架构设计"
    
    print(f"\n任务 1: {simple_task}")
    model = router.route_by_complexity(simple_task)
    print(f"选中：{type(model).__name__}")
    
    print(f"\n任务 2: {complex_task}")
    model = router.route_by_complexity(complex_task)
    print(f"选中：{type(model).__name__}")


def test_fallback_chain():
    """测试降级链 - 云端失败时使用本地"""
    print("\n" + "=" * 60)
    print("降级链 (Fallback Chain)")
    print("=" * 60)
    
    # 创建不同优先级的模型
    primary_model = None
    fallback_model = ChatOllama(model="qwen3.5:9b")
    
    if os.getenv('ANTHROPIC_API_KEY'):
        primary_model = ChatAnthropic(model="claude-3-sonnet-20240229")
        print("主模型：Anthropic Claude")
    elif os.getenv('OPENAI_API_KEY'):
        primary_model = ChatOpenAI(model="gpt-3.5-turbo")
        print("主模型：OpenAI GPT")
    else:
        print("主模型：无，直接使用降级模型")
    
    print(f"降级模型：Ollama Qwen3.5")
    
    # 创建调用函数
    def call_with_fallback(messages):
        """先尝试主模型，失败则使用降级模型"""
        if primary_model:
            try:
                print("\n尝试主模型...")
                return primary_model.invoke(messages)
            except Exception as e:
                print(f"主模型失败：{e}")
                print("切换到降级模型...")
        
        return fallback_model.invoke(messages)
    
    # 测试
    from langchain_core.messages import HumanMessage
    messages = [HumanMessage(content="请用一句话解释什么是 API。")]
    
    response = call_with_fallback(messages)
    print(f"\n响应：{response.content}")


def test_cost_optimization():
    """测试成本优化策略"""
    print("\n" + "=" * 60)
    print("成本优化策略")
    print("=" * 60)
    
    print("""
    💰 成本优化建议:
    
    1. 开发阶段:
       - 使用 Ollama 本地模型 (免费)
       - 减少不必要的 API 调用
       - 缓存常用响应
    
    2. 测试阶段:
       - 使用较小/较便宜的模型 (如 haiku, gpt-3.5)
       - 限制 token 数量
       - 批量处理请求
    
    3. 生产阶段:
       - 根据任务复杂度路由
       - 简单任务用便宜模型
       - 复杂任务用强大模型
    
    4. 监控:
       - 跟踪 token 使用量
       - 设置预算告警
       - 定期审查使用模式
    """)
    
    # 示例：根据 token 限制选择模型
    def select_model_by_token_limit(estimated_tokens: int):
        """根据预估 token 数选择模型"""
        if estimated_tokens < 500:
            return "ollama (本地，免费)"
        elif estimated_tokens < 2000:
            return "claude-3-haiku 或 gpt-3.5-turbo (经济)"
        else:
            return "claude-3-sonnet 或 gpt-4 (强大)"
    
    print("\n📊 模型选择示例:")
    for tokens in [100, 1000, 5000]:
        model = select_model_by_token_limit(tokens)
        print(f"  {tokens} tokens → {model}")


def test_multi_model_comparison():
    """测试多模型对比"""
    print("\n" + "=" * 60)
    print("多模型对比")
    print("=" * 60)
    
    router = ModelRouter()
    
    if len(router.models) < 2:
        print("需要至少 2 个模型才能对比")
        return
    
    question = "什么是机器学习？请用一句话解释。"
    from langchain_core.messages import HumanMessage
    messages = [HumanMessage(content=question)]
    
    print(f"\n问题：{question}\n")
    
    for name, model in router.models.items():
        try:
            print(f"{name.upper()} 模型:")
            response = model.invoke(messages)
            print(f"  {response.content}\n")
        except Exception as e:
            print(f"  ❌ 调用失败：{e}\n")


if __name__ == "__main__":
    print("\n🔄 模型切换与路由示例\n")
    
    test_model_router()
    test_fallback_chain()
    test_cost_optimization()
    test_multi_model_comparison()
    
    print("\n✅ 所有测试完成！")
