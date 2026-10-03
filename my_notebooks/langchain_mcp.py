# 1.加载环境变量


import asyncio
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
load_dotenv()

# 2.初始化模型

async def main():
    qwen_model = init_chat_model("openai:qwen3.7-plus", temperature=0, base_url=os.getenv("ROOT_URL"))
    # 3.定义工具，用MCP获取工具
    # 3.1.定义mcp client
    mcp_config = {
    "mcpServers": {
        "time": {
        "transport": "stdio",
        "command": "uvx",
        "args": [
            "mcp-server-time",
            "--local-timezone=America/New_York"
        ]
        }
    }
    }
    async with MCPAdapter(mcp_config) as adapter:
        tools = await adapter.list_tools()
        agent = create_agent(qwen_model, tools)
        result = await agent.ainvoke({"messages": [HumanMessage("现在是什么时间")]})
        print(result)  # <-- print the result
        return result

if __name__ == "__main__":
    asyncio.run(main())