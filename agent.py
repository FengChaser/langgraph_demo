"""
LangGraph 简洁版工具集成智能体

使用 create_react_agent 预构建方法，代码更简洁、更易维护。
"""

import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.pydantic_v1 import BaseModel, Field
# 导入我们的工具
from tools import AVAILABLE_TOOLS
        
# 加载环境变量
load_dotenv()

class SimpleToolAgent(BaseModel):       
    """简洁版工具集成智能体"""
    
    def __init__(self):
        # 初始化大模型
        self.model = ChatDeepSeek(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            model=os.getenv("MODEL_NAME", "deepseek-chat"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2000"))
        )
        
        # 创建内存检查点
        self.memory = MemorySaver()
        
        # 使用 create_react_agent 创建智能体 - 就这么简单！
        self.agent = create_react_agent(
            model=self.model,
            tools=AVAILABLE_TOOLS,
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

def main():
    """主函数 - 演示简洁版智能体的使用"""
    print("🤖 LangGraph 简洁版工具智能体启动中...")
    print("💡 提示：输入 'quit' 或 'exit' 退出程序")
    print("🔧 可用工具：天气查询、计算器、时间查询、文本处理、随机数生成、单位转换")
    print("=" * 70)
    
    try:
        # 创建智能体 - 就这一行！
        agent = SimpleToolAgent()
        print("✅ 智能体初始化成功！")
        
        # 显示示例用法
        print("\n📝 示例用法：")
        print("- 查询天气：'北京今天天气怎么样？'")
        print("- 数学计算：'计算 2^10 + sqrt(144)'")
        print("- 时间查询：'现在几点了？'")
        print("- 文本处理：'统计这段文字的字数：Hello World'")
        print("- 随机数：'生成一个1到100的随机数'")
        print("- 单位转换：'100厘米等于多少米？'")
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

if __name__ == "__main__":
    main()