import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from utils.config import ENV_PATH

load_dotenv(ENV_PATH)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# =========== haiku ===========
haiku_llm = ChatAnthropic(
    model="claude-haiku-4-5",
    anthropic_api_key=ANTHROPIC_API_KEY,
    max_tokens=2000
)

# =========== sonnet ===========
sonnet_llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key=ANTHROPIC_API_KEY,
    max_tokens=2000
)

# =========== opus ===========
opus_llm = ChatAnthropic(
    model="claude-opus-4-8",
    anthropic_api_key=ANTHROPIC_API_KEY,
    max_tokens=2000
)

if __name__ == "__main__":
    question = "Design one python class to use a multimodal model summarize image. Make it simple but production grade."
    print(f"Question: \n {question}")

    haiku_response = haiku_llm.invoke([HumanMessage(content=question)])

    print(f"haiku response: \n {haiku_response.content}")

    sonnet_response = sonnet_llm.invoke([HumanMessage(content=question)])

    print(f"sonnet response: \n {sonnet_response.content}")

    opus_response = opus_llm.invoke([HumanMessage(content=question)])

    print(f"opus response: \n {opus_response.content}")