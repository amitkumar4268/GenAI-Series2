# Deployment Guide

## Local Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Create `.env` from `.env.example` and set `OPENAI_API_KEY`.
3. Run:
   `python apps/5_pdf_qna_gradio.py`

## Hugging Face Spaces (Gradio)
1. Create a new Gradio Space.
2. Upload these files/folders:
   - `app.py`
   - `requirements.txt`
   - `apps/5_pdf_qna_gradio.py`
3. In Space settings, add secret:
   - `OPENAI_API_KEY`
4. Deploy and test with sample PDFs.

## Render / Railway
1. Create a Python service from this repository.
2. Install command:
   `pip install -r requirements.txt`
3. Start command:
   `python app.py`
4. Set environment variable:
   - `OPENAI_API_KEY`
