import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from tools.equity_signal import equity_signal_analyzer
from tools.portfolio_risk import portfolio_risk_analyzer
from tools.news_sentiment import news_sentiment_analyzer
from utils.config import ENV_PATH

# ---- create system prompt with skills ----
def load_skills():
    paths = [
        "skills/equity_signal.md",
        "skills/portfolio_risk.md",
        "skills/news_sentiment.md",
    ]
    return "\n\n------------\n\n".join(open(p).read() for p in paths)

skills_text = load_skills()

SYSTEM_PROMPT = f"""
You are a financial AI agent.

Available Skills:
{skills_text}

Rules:
- If the user mentions multiple tickers with weights/allocation → use portfolio_risk_analyzer
- If the user asks about news, sentiment, or headlines → use news_sentiment_analyzer 
- If the user asks about trend, signal, or a single stock → use equity_signal_analyzer
- You MAY use multiple skills if needed
- If the task requires multiple steps, call tools sequentially
- Combine results into a final answer
- Follow its rules strictly
- Output must be valid JSON
- NEVER wrap output in markdown code fences (no backticks)
- NEVER ask for clarification — always infer the correct skill from context
"""

# ---- create llm ----
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0
)

# ---- create tools ----
tools = [equity_signal_analyzer, portfolio_risk_analyzer, news_sentiment_analyzer]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


if __name__ == "__main__":
    import json, re

    # content = "GOOGLE trend"
    # content = "Salesforce trend and sentiment analysis"
    # content = "Analyze below holdings: NVDA 25%, ADBE 45%, ALIBABA 20%, TENCENT 5%, QQQ 5%"
    # content = "What about the portfolio risk with half Microsoft and hal Intel?"
    content = "Analyze Nvidia's sentiment"

    result = agent.invoke({"messages": [HumanMessage(content=content)]})

    print(f"result is {result}")

    last_message = result["messages"][-1]
    if not isinstance(last_message, AIMessage):
        print("last message is not AIMessage")
    print(last_message.content)