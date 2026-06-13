import asyncio
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from claude_practice import haiku_llm


async def main():

    # 1. Initialize the Claude LLM
    llm = haiku_llm

    # 2. Initialize the MCP Client
    # This tells LangChain how to start and connect to your local MCP server
    mcp_client = MultiServerMCPClient({
        "local_tools": {
            "command": "python",
            "args": ["mcp_server.py"],
            "transport": "stdio"
        }
    })

    # 3. Fetch tools from the MCP server and convert them to LangChain tools
    print("Connecting to MCP Server and loading tools...")
    tools = await mcp_client.get_tools()
    print(f"Loaded {len(tools)} tools: {[tool.name for tool in tools]}")

    # 4. Define the Agent Prompt
    prompt = SystemMessage(content = "You are a helpful AI assistant. Use the provided tools to accomplish tasks. Always verify your work if possible.")

    # 5. Create the Agent and Executor
    agent = create_agent(
        model = llm,
        tools = tools,
        system_prompt = prompt,
    )

    print(agent.get_graph().draw_ascii())

    # 6. Test the Agent with a prompt that requires BOTH tools
    test_prompt = (
        "Calculate the result of twenty three multiplies eleven. "
        "Then, write that final number to a file named 'math_result.txt'. "
        "Finally, read the file back to me to confirm it was saved correctly."
    )

    print("\n--- Running Agent ---")
    response = await agent.ainvoke({"messages": [HumanMessage(content=test_prompt)]})

    print("\n--- Final Output ---")
    final_message = response["messages"][-1]
    print(final_message.content)
    print(f"response details: {response}")


if __name__ == "__main__":
    asyncio.run(main())