from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from Agent.tools.finance_tools import (
    get_user_spend,
    get_user_spend_by_category
)

tools = [get_user_spend, get_user_spend_by_category]


llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1000,
    temperature=0,
    system="You are an asistant  with knwoledge in personal financial topics with some tools",
)

llm = ChatOpenAI(
     model="gpt-4o",
     temperature=0,
     
)


llm_with_tools = llm.bind_tools(tools)



def run_agent(state: dict):
    """
    Run the finance agent with the provided message.
    Args:
        state (dict): The message to send to the agent.
    Returns:
        str: The response from the agent.
    """
    # response = llm_with_tools.invoke([{"role": "user",
    #                                         "content": message+f"user email is :{email}"}#,
    #                                         #{"role": "system",
    #                                          #"content": "user email is:"+ email}
    #                                          ])
    print(state)
    print(state["messages"])
    print(state["messages"][0].content)
    print(state["messages"][0].content+state["email"])
    response = llm_with_tools.invoke([{"role":"system", "content": "You are an asistant  with knwoledge in personal financial topics with some tools"}]+state["messages"]+[SystemMessage("the email of the user is: "+ state["email"])])
    print(f"messages: {state["messages"]}", f"email: {state["email"]}")

    print("responseRUNAGENT: ", response)
    return response