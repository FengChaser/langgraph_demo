# LangGraph 智能体项目

这是一个使用 LangGraph 构建智能体的项目，集成了 DeepSeek 大模型。

## 环境设置

1. 激活虚拟环境：
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 项目结构

- `venv/` - Python虚拟环境
- `requirements.txt` - 项目依赖
- `agent.py` - 主要的智能体代码（待创建）
- `.env` - 环境变量配置（待创建）

## 使用说明

1. 在 `.env` 文件中配置 DeepSeek API 密钥
2. 运行 `python agent.py` 启动智能体

## 已安装的包

- langgraph==0.4.8 - 用于构建状态化的多智能体应用
- langchain-core - LangChain 核心组件
- 其他相关依赖包