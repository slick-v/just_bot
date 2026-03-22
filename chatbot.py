from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain.memory  import ConversationBufferMemory

from langgraph.graph import StateGraph,END
from langchain_core.messages import HumanMessage, AIMessage


from state import AgentState
from tools import caluculator

# Load Model
llm = ChatOllama(model="llama3")

# agent_Node
def agent_node(state:AgentState):

    messages = state["messages"]

    user_message = messages[-1].content

    # simple tool logic
    if any(op in user_message for op in ["+", "-", "*", "/"]):

        tool_result = caluculator(user_message)

        response = llm.invoke(f"caluculator result is {tool_result}, expalain it")
    else:
        response = llm.invoke(user_message)

    messages.append(AIMessage(content=response.content))

    return {"messages": messages}

# graph_node

graph =StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app =graph.compile()


# chat loop

state = {"messages": []}
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    state["messages"].append(
       HumanMessage(content=user_input)

   )
    state = app.invoke(state)

    print("Bot : ", state["messages"][-1].content)


   