
from Agent import finance_agent
from Agent.tools.finance_tools import (
    get_user_spend,
    get_user_spend_by_category
)

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic


class MessagesState(MessagesState):
    email: str
    llm_response: str




tools = [get_user_spend, get_user_spend_by_category]

    

def toolsedge(state): #-> Literal["tools", "response"]:
    response = tools_condition(state)
    if response == "__end__":
        return "response_node"
    return response

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "response_node"

def first_node(state):
    state["messages"].append({"role":"system"})

def finance_agent_node(state: MessagesState) -> MessagesState:
    response = finance_agent.run_agent(state)
    if response.content:
        state["messages"].append({"role":"assistant", "content":response.content})
    #{"messages": [finance_agent.run_agent(state)]}
    return state

def response_node(state: MessagesState) -> MessagesState:
    print(state, "\n\n")
    response_llm = ChatAnthropic(model="claude-3-7-sonnet-20250219",
    max_tokens=1000,
    temperature=0,
    system="You task is getting the contex of the state retrive the answer to the user in natural way",)
    response = response_llm.invoke(state["messages"])
    state["llm_response"] = response.content
    return state 

builder = StateGraph(MessagesState)

builder.add_node("finance_agent_node", finance_agent_node)
builder.add_node("response_node", response_node)
builder.add_node("tools", ToolNode(tools))


builder.add_edge(START, "finance_agent_node")
builder.add_conditional_edges("finance_agent_node", toolsedge, ["response_node", "tools"])
builder.add_edge("response_node", END)

graph = builder.compile()