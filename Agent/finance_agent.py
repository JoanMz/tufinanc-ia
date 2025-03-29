from langchain_anthropic import Anthropic

llm = Anthropic(
    model="claude-3-5-haiku-20241022",
    max_tokens=1000,
    temperature=1,
    system="You are a personal financial advisor.",
)

llm_with_tools = llm.bind_tools()