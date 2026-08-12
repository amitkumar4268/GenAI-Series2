from os import getenv
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

try:
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Missing dependency. Run this script with the project venv Python: " 
        "c:/Users/amitk/Desktop/learning/GenAI-Series2/.venv/Scripts/python.exe -m streamlit run apps/1_qna_bot.py"
    ) from exc

load_dotenv()
api_key = getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")

llm = ChatOpenAI(model="gpt-5.6", api_key=api_key)

if get_script_run_ctx() is None:
    print("Run this app in browser using:")
    print("c:/Users/amitk/Desktop/learning/GenAI-Series2/.venv/Scripts/python.exe -m streamlit run c:/Users/amitk/Desktop/learning/GenAI-Series2/apps/1_qna_bot.py")
else:
    st.title("Ask Buddy with Amit Kumar")
    st.markdown("Chat Bot with Amit Kumar !")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = message.get("role")
        content = message.get("content")
        st.chat_message(role).markdown(content)

    query = st.chat_input("Ask anything?")
    if query:
        st.chat_message("user").markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})
        try:
            with st.spinner("Thinking..."):
                response = llm.invoke(query)

            content = getattr(response, "content", "")
            if isinstance(content, str):
                assistant_text = content
            elif isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if text:
                            parts.append(str(text))
                    else:
                        parts.append(str(item))
                assistant_text = "\n".join(parts).strip()
            else:
                assistant_text = str(content)

            if not assistant_text:
                assistant_text = "I could not parse a text response from the model."

            st.chat_message("assistant").markdown(assistant_text)
            st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        except Exception as exc:
            st.error(f"LLM call failed: {exc}")