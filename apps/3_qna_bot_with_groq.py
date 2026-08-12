from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
import streamlit as st

model = ChatGroq(model="openai/gpt-oss-20b", streaming=True)
search = GoogleSerperAPIWrapper()

if 'memory' not in st.session_state:
    st.session_state.memory = MemorySaver()
    st.session_state.history = []
    #memory = st.session_state.memory

agent = create_agent(
    model=model,
    tools=[search.run],
    checkpointer=st.session_state.memory,
    system_prompt="You are a helpful assistant that can answer questions using Google Search results."
)
st.subheader("Google Search Agent with Groq")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content) 

query = st.chat_input("Ask to your Assistant ")

if query:
    st.chat_message("User").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    if query.lower() in ["exit", "quit", "bye"]:
        st.write("Goodbye!")
        st.stop()

    response = agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "1"}},
        stream_mode = "messages"
    )

    ai_container = st.chat_message("AI")
    with ai_container:
        space = st.empty()

        message = ""

        for chunk in response:          
            message =   message + chunk[0].content
            space.write(message)
       
    #answer = response['messages'][-1].content
    #st.chat_message("AI").markdown(answer)

    st.session_state.history.append({"role": "AI", "content": message})
