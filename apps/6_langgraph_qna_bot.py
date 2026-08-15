from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated, Any

class ChatState(BaseModel):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="openai/gpt-oss-20b")

def chatBotNode(state: ChatState) -> ChatState:
   response = llm.invoke(state.messages)
   state.messages = [response]
   return state

memory = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node('chatBot',chatBotNode)

graph.add_edge(START, 'chatBot')
graph.add_edge('chatBot', END)

graph = graph.compile(checkpointer=memory)
config = {"configurable":{"thread_id":"my_bit_1"}}

while True:
    query = input("User: ")

    if query.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat. Goodbye!")
        break

    response = graph.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config
    )

    ans = response['messages'][-1].content
    print("AI: " + ans)