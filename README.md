# GenAI-Series2

This repository contains hands-on GenAI examples and apps using LangChain.

## PDF Q&A Chatbot (Gradio)

The file `apps/5_pdf_qna_gradio.py` provides a conversational chatbot that:

- Uploads one or more PDF files
- Splits content into chunks
- Creates embeddings and vector search index (Chroma)
- Retrieves relevant context for each question
- Responds with grounded answers and source references

### Setup

1. Create/activate your virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can also enter the key directly in the Gradio UI.

### Run

```bash
python apps/5_pdf_qna_gradio.py
```

Then open the local Gradio URL shown in the terminal.

### Suggested Deployment

- Hugging Face Spaces (Gradio)
- Render or Railway with Python runtime

For deployment, include `requirements.txt` and ensure `OPENAI_API_KEY` is configured in environment variables.