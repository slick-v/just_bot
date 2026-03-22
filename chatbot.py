from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain.memory  import ConversationBufferMemory



# Load Model
llm = ChatOllama(model="llama3")


# memory
memory = ConversationBufferMemory(return_messages=True)

# caluculator tool
def caluculator(expression: str):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid math expression"


# define prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You Are a helpful Ai Assisitant, "
    "if  user asks math question, use the caluculator provided,"
    "expalin the reson clearly"),

    # memory will be inserted here
    MessagesPlaceholder(variable_name="history"),

    ("human" , "{question}")

])


# connect prompt -> model
chain = prompt | llm


# chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # simple logic to detect math expression
    if any(op in user_input for op in ["+" , "-", "*" , "/"]):

        tool_result = caluculator(user_input)

        user_input =  f"""
        user question: {user_input}
        calucualtor result: {tool_result}
        explain the result

    """

    # load history from memory
    history = memory.load_memory_variables({})["history"]

    # get response
    response = chain.invoke({
        "question" : user_input,
        "history": history
    })

    # response = chain.invoke({"question" : user_input})

    print("Bot : ", response.content)


    # save conversation to memory
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )