# Assignment Submission: Conversational PDF Q&A Chatbot

## Situation
The assignment requires building a practical conversational assistant that answers questions using information extracted from PDF documents. The expected output is not only a working application, but also a clear explanation of the pipeline and a structured report using Situation, Task, Action, and Result.

## Task
I had to design and implement an end-to-end Retrieval-Augmented Generation (RAG) chatbot with these requirements:

- Extract text content from uploaded PDF files
- Convert text into embeddings (numerical vectors)
- Retrieve relevant chunks for each user query
- Generate grounded answers with an LLM
- Provide a simple and usable Gradio interface
- Prepare the project for practical deployment
- Document analysis and interpretation for LMS submission

## Action
### A. Learning and Design Review
- Reviewed course learning flow for RAG (document loading, splitting, embeddings, retrieval, and response generation).
- Aligned implementation with Gradio app patterns for file upload, state handling, and chat interaction.

### B. Data Extraction and Preprocessing
- Implemented PDF upload in the UI (`multiple` files supported).
- Loaded PDF content using `PyPDFLoader`.
- Split text with `RecursiveCharacterTextSplitter`.
- Added configurable controls for chunk size and chunk overlap.

### C. Vectorization and Indexing
- Generated embeddings with `OpenAIEmbeddings` using `text-embedding-3-small`.
- Stored vectors in `Chroma` for semantic retrieval.
- Added configurable `top_k` retrieval to tune context breadth.

### D. Answer-Finding Mechanism
- Built an answer chain using `RetrievalQA` with `chain_type="stuff"`.
- Used a prompt that enforces context-grounded answers and concise responses.
- Returned source references (file name + page number) to support traceability.

### E. User Interface and Interaction
- Built a Gradio app with:
  - PDF uploader
  - Optional API key input (with `.env` fallback)
  - Model and retrieval controls
  - Knowledge-base build button and status output
  - Chat panel with send and clear options

### F. Deployment and Packaging
- Added `gradio` to dependencies.
- Added `app.py` entrypoint for hosting platforms.
- Added deployment guide for local run, Hugging Face Spaces, and Render/Railway.

## Result
The project now provides a working conversational PDF chatbot that:

- Accepts one or more PDF files from users
- Builds a retrievable semantic knowledge base from uploaded content
- Answers questions using retrieved evidence from the PDFs
- Displays source citations to improve transparency and trust
- Can be run locally and prepared for cloud deployment

## Analysis and Interpretation
### 1. Retrieval Quality
Retrieval quality depends strongly on chunking settings and `top_k`. If chunks are too small, answers lose context. If chunks are too large, retrieval becomes noisy. A balanced default improves answer relevance.

### 2. Model-Cost Tradeoff
Using a compact chat model (default: `gpt-4o-mini`) offers faster latency and lower cost for interactive demos while still supporting useful grounded responses.

### 3. Reliability and Explainability
Source references improve explainability because users can verify where answers came from. This also helps identify weak retrieval when answers are incomplete.

### 4. Scalability Consideration
For larger document collections, persistent vector storage and pre-indexing should be used to avoid rebuilding embeddings each run.

## Files Included in Submission
- `apps/5_pdf_qna_gradio.py`
- `app.py`
- `requirements.txt`
- `README.md`
- `DEPLOYMENT.md`
- `ASSIGNMENT_SUBMISSION.md`

## Execution Steps
1. Install dependencies:
  `pip install -r requirements.txt`
2. Configure environment:
  add `OPENAI_API_KEY` in `.env` (or provide in UI)
3. Run app:
  `python apps/5_pdf_qna_gradio.py`
4. Upload PDF files, click **Build Knowledge Base**, and ask questions.

## LMS Checklist (Strict)
- Situation section completed
- Task section completed
- Action section completed with implementation details
- Result section completed with outcomes
- Analysis and interpretation included
- Gradio-based chatbot implementation included
- Deployment notes included

## Submission Note
Direct LMS upload must be done manually by the student account holder. All required project files and analysis content are prepared in this repository.
