"""
LangGraph 简洁版工具集成智能体

使用 create_react_agent 预构建方法，代码更简洁、更易维护。
支持自定义工具和 LangChain 内置工具。
"""

import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# 导入我们的工具
from tools import AVAILABLE_TOOLS
from langchain_tools import get_available_tools

# 加载环境变量
load_dotenv()

class SimpleToolAgent:
    """简洁版工具集成智能体"""
    
    def __init__(self, use_langchain_tools: bool = True):
        """
        初始化智能体
        
        Args:
            use_langchain_tools: 是否使用 LangChain 内置工具
        """
        # 初始化大模型
        self.model = ChatDeepSeek(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            model=os.getenv("MODEL_NAME", "deepseek-chat"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2000"))
        )
        
        # 创建内存检查点
        self.memory = MemorySaver()
        
        # 组合工具列表
        all_tools = AVAILABLE_TOOLS.copy()
        
        if use_langchain_tools:
            try:
                langchain_tools = get_available_tools()
                all_tools.extend(langchain_tools)
                print(f"✅ 已加载 {len(langchain_tools)} 个 LangChain 内置工具")
            except Exception as e:
                print(f"⚠️ LangChain 工具加载失败: {e}")
        
        self.tools = all_tools
        
        # 使用 create_react_agent 创建智能体 - 就这么简单！
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            checkpointer=self.memory
        )
    
    def chat(self, message: str, thread_id: str = "default"):
        """与智能体对话"""
        config = {"configurable": {"thread_id": thread_id}}
        
        # 直接调用智能体
        result = self.agent.invoke(
            {"messages": [("user", message)]},
            config=config
        )
        
        # 返回最后一条AI消息
        return result["messages"][-1].content
    
    def get_conversation_history(self, thread_id: str = "default"):
        """获取对话历史"""
        config = {"configurable": {"thread_id": thread_id}}
        
        # 获取当前状态
        current_state = self.agent.get_state(config)
        
        if current_state and current_state.values:
            return current_state.values.get("messages", [])
        return []
    
    def list_tools(self):
        """列出所有可用工具"""
        print(f"\n🔧 可用工具列表 (共 {len(self.tools)} 个):")
        print("=" * 60)
        
        # 分类显示工具
        custom_tools = []
        langchain_tools = []
        
        for tool in self.tools:
            if hasattr(tool, 'name'):
                if tool.name in ['get_weather', 'calculate', 'get_datetime_info', 
                               'process_text', 'generate_random', 'convert_units', 'search_web']:
                    custom_tools.append(tool)
                elif tool.name == 'serpapi_search':
                    langchain_tools.append(tool)
        
        if custom_tools:
            print("📦 自定义工具:")
            for tool in custom_tools:
                print(f"  • {tool.name}: {tool.description}")
        
        if langchain_tools:
            print("\n🔗 LangChain 内置工具:")
            for tool in langchain_tools:
                print(f"  • {tool.name}: {tool.description}")
        
        print("=" * 60)

def main():
    """主函数 - 演示简洁版智能体的使用"""
    print("🤖 LangGraph 简洁版工具智能体启动中...")
    print("💡 提示：输入 'quit' 或 'exit' 退出程序")
    print("=" * 70)
    
    try:
        # 创建智能体 - 支持 LangChain 内置工具
        agent = SimpleToolAgent(use_langchain_tools=True)
        print("✅ 智能体初始化成功！")
        
        # 显示可用工具
        agent.list_tools()
        
        # 显示示例用法
        print("\n📝 示例用法：")
        print("🌤️  天气查询：'北京今天天气怎么样？'")
        print("🧮 数学计算：'计算 2^10 + sqrt(144)'")
        print("⏰ 时间查询：'现在几点了？'")
        print("📝 文本处理：'统计这段文字的字数：Hello World'")
        print("🎲 随机数：'生成一个1到100的随机数'")
        print("📏 单位转换：'100厘米等于多少米？'")
        print("🔍 网络搜索：'搜索Python编程教程'")
        print("=" * 70)
        
        # 对话循环
        while True:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            try:
                # 获取回复
                print("🤔 思考中...")
                response = agent.chat(user_input)
                print(f"🤖 助手: {response}")
                
            except Exception as e:
                print(f"❌ 出错了: {e}")
                print("请检查你的网络连接和API配置。")
    
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n请确保：")
        print("1. 已创建 .env 文件并配置了 DEEPSEEK_API_KEY")
        print("2. 网络连接正常")
        print("3. API密钥有效")
        print("4. 如需使用搜索功能，请设置 SERPAPI_API_KEY")

if __name__ == "__main__":
    main()