import os

import gradio as gr
from dotenv import load_dotenv
from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate


SYSTEM_PROMPT = """
You are an assistant for question-answering tasks.
Use the provided document context to answer the question.
If the answer is not in the context, clearly say you do not know.
Keep the answer concise and useful.

Context:
{context}
Question: {question}
""".strip()


def build_knowledge_base(pdf_files, openai_api_key, model_name, temperature, chunk_size, chunk_overlap, top_k):
    try:
        if not pdf_files:
            return "Please upload at least one PDF file.", None

        load_dotenv()

        # User can give API key in UI or use .env file.
        api_key = ""
        if openai_api_key:
            api_key = openai_api_key.strip()
        if api_key == "":
            api_key = os.getenv("OPENAI_API_KEY", "").strip()

        if api_key == "":
            return "Missing OpenAI API key. Add it in UI or in .env", None

        all_docs = []
        for one_pdf in pdf_files:
            loader = PyPDFLoader(one_pdf)
            docs = loader.load()
            all_docs.extend(docs)

        if len(all_docs) == 0:
            return "No readable text was found in the uploaded PDFs.", None

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(chunk_size),
            chunk_overlap=int(chunk_overlap),
        )
        split_docs = splitter.split_documents(all_docs)

        embed_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=api_key,
        )

        vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=embed_model,
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": int(top_k)})

        llm = ChatOpenAI(
            model=model_name,
            temperature=float(temperature),
            api_key=api_key,
        )

        prompt = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=["context", "question"],
        )

        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        kb_state = {
            "chain": rag_chain,
            "total_chunks": len(split_docs),
        }

        names = []
        for path in pdf_files:
            names.append(os.path.basename(path))

        status = "Knowledge base ready from " + str(len(pdf_files)) + " file(s): "
        status += ", ".join(names)
        status += ". Created " + str(len(split_docs)) + " chunks."

        return status, kb_state

    except Exception as e:
        return "Failed to build knowledge base: " + str(e), None


def answer_question(question, chat_history, kb_state):
    history = chat_history or []

    # Convert old tuple-style history to Gradio message format if needed.
    normalized_history = []
    for item in history:
        if isinstance(item, dict):
            normalized_history.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            normalized_history.append({"role": "user", "content": str(item[0])})
            normalized_history.append({"role": "assistant", "content": str(item[1])})

    history = normalized_history

    if not question or question.strip() == "":
        return "", history

    clean_question = question.strip()
    history.append({"role": "user", "content": clean_question})

    if kb_state is None or "chain" not in kb_state:
        msg = "Please upload PDF files and click Build Knowledge Base first."
        history.append({"role": "assistant", "content": msg})
        return "", history

    try:
        result = kb_state["chain"].invoke({"query": clean_question})
        answer = result.get("result", "I could not generate an answer.")

        context_docs = result.get("source_documents", [])
        source_list = []

        for doc in context_docs:
            source_name = os.path.basename(doc.metadata.get("source", "Unknown source"))
            page_no = doc.metadata.get("page")
            if isinstance(page_no, int):
                source_text = source_name + " (page " + str(page_no + 1) + ")"
            else:
                source_text = source_name

            if source_text not in source_list:
                source_list.append(source_text)

        if len(source_list) > 0:
            answer += "\n\nSources:"
            for one_source in source_list:
                answer += "\n- " + one_source

        history.append({"role": "assistant", "content": answer})
        return "", history

    except Exception as e:
        history.append({"role": "assistant", "content": "Failed to answer the question: " + str(e)})
        return "", history


load_dotenv()

with gr.Blocks(title="PDF Q&A Chatbot with Gradio") as demo:
    gr.Markdown(
        """
        # Conversational PDF Q&A Chatbot
        Upload one or more PDF files, build a retrieval index, and ask questions grounded in document context.
        """
    )

    kb_state = gr.State(value=None)

    with gr.Row():
        with gr.Column(scale=1):
            pdf_files = gr.File(
                label="Upload PDF Files",
                file_types=[".pdf"],
                file_count="multiple",
                type="filepath",
            )
            api_key = gr.Textbox(
                label="OpenAI API Key",
                placeholder="sk-... (or set OPENAI_API_KEY in .env)",
                type="password",
            )
            model_name = gr.Dropdown(
                label="Model",
                choices=["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1"],
                value="gpt-4o-mini",
            )
            temperature = gr.Slider(
                label="Temperature",
                minimum=0.0,
                maximum=1.0,
                value=0.2,
                step=0.1,
            )
            chunk_size = gr.Slider(
                label="Chunk Size",
                minimum=400,
                maximum=2000,
                value=1000,
                step=100,
            )
            chunk_overlap = gr.Slider(
                label="Chunk Overlap",
                minimum=0,
                maximum=400,
                value=150,
                step=25,
            )
            top_k = gr.Slider(
                label="Retriever Top-K",
                minimum=1,
                maximum=10,
                value=4,
                step=1,
            )

            build_button = gr.Button("Build Knowledge Base", variant="primary")
            status_box = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Chat", height=540)
            question_box = gr.Textbox(
                label="Ask a Question",
                placeholder="What are the main findings in the report?",
            )
            send_button = gr.Button("Send", variant="primary")
            clear_button = gr.Button("Clear Chat")

    build_button.click(
        fn=build_knowledge_base,
        inputs=[pdf_files, api_key, model_name, temperature, chunk_size, chunk_overlap, top_k],
        outputs=[status_box, kb_state],
    )

    send_button.click(
        fn=answer_question,
        inputs=[question_box, chatbot, kb_state],
        outputs=[question_box, chatbot],
    )

    question_box.submit(
        fn=answer_question,
        inputs=[question_box, chatbot, kb_state],
        outputs=[question_box, chatbot],
    )

    clear_button.click(fn=lambda: [], outputs=[chatbot])

if __name__ == "__main__":
    demo.launch()
