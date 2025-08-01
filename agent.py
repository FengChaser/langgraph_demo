"""
LangGraph 智能体示例 - 集成 DeepSeek 大模型

这个示例展示了如何使用 LangGraph 创建一个简单的智能体，
该智能体可以进行对话并具有记忆功能。
"""

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# 加载环境变量
load_dotenv()

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

class LangGraphAgent:
    """LangGraph 智能体类"""
    
    def __init__(self):
        # 使用 LangChain 官方的 ChatDeepSeek 组件
        self.llm = ChatDeepSeek(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            model=os.getenv("MODEL_NAME", "deepseek-chat"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "1000"))
        )
        self.memory = MemorySaver()
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """创建 LangGraph 工作流"""
        
        def chatbot_node(state: AgentState):
            """聊天机器人节点"""
            messages = state["messages"]
            
            # 添加系统提示
            system_prompt = """你是一个友好且有帮助的AI助手。请用中文回答用户的问题。
你可以：
1. 回答各种问题
2. 进行日常对话
3. 提供建议和帮助
4. 记住之前的对话内容

请保持友好、专业的态度。"""
            
            # 如果是第一条消息，添加系统提示
            if len(messages) == 1:
                messages = [SystemMessage(content=system_prompt)] + messages
            
            # 调用大模型
            response = self.llm.invoke(messages)
            return {"messages": [response]}
        
        # 创建图
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("chatbot", chatbot_node)
        
        # 设置入口点
        workflow.set_entry_point("chatbot")
        
        # 设置结束点
        workflow.add_edge("chatbot", END)
        
        # 编译图
        return workflow.compile(checkpointer=self.memory)
    
    def chat(self, message: str, thread_id: str = "default"):
        """与智能体对话"""
        config = {"configurable": {"thread_id": thread_id}}
        
        # 创建用户消息
        user_message = HumanMessage(content=message)
        
        # 运行图
        result = self.graph.invoke(
            {"messages": [user_message]},
            config=config
        )
        
        # 返回最后一条AI消息
        return result["messages"][-1].content
    
    def get_conversation_history(self, thread_id: str = "default"):
        """获取对话历史"""
        config = {"configurable": {"thread_id": thread_id}}
        
        # 获取当前状态
        current_state = self.graph.get_state(config)
        
        if current_state and current_state.values:
            return current_state.values.get("messages", [])
        return []

def main():
    """主函数 - 演示智能体的使用"""
    print("🤖 LangGraph + DeepSeek 智能体启动中...")
    print("💡 提示：输入 'quit' 或 'exit' 退出程序")
    print("=" * 50)
    
    try:
        # 创建智能体
        agent = LangGraphAgent()
        print("✅ 智能体初始化成功！")
        
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