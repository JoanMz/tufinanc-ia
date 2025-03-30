from langchain_anthropic import ChatAnthropic
from Agent.tools.finance_tools import (
    get_user_spend
)


tools = [
        get_user_spend
        ]


llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    max_tokens=1000,
    temperature=1,
    system="You are a personal financial advisor.",
)



llm_with_tools = llm


class FinanceAgent:
    """
    This class represents a finance agent that interacts with a database to retrieve user spending information.
    """
    def __init__(self, db_connection):
        self._tools = [tools]
        self.llm = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=1,
            system="You are a personal financial advisor.",
        )
        self.llm_with_tools = self.llm.bind_tools(self._tools)

    def run_agent(self, message: str, email: str):
        """
        Run the finance agent with the provided message.
        Args:
            message (str): The message to send to the agent.
        Returns:
            str: The response from the agent.
        """
        response = self.llm_with_tools.invoke([{"role": "user",
                                                "content": message},
                                                {"role": "system",
                                                 "content": "user email is:"+ email}])
        return response