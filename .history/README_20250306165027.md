# repo-249-Resume-Review-Agent
here giving my doc

# Resume Coach

A full-stack agentic platform that allows users to upload their resume and receive personalized career feedback, next steps, and advice powered by AI.

## Architecture
- **Frontend**: React + Vite for a fast, modern UI with a focus on UX.
- **Backend**: FastAPI (Python) for handling file uploads and API endpoints.
- **AI**: Python class using the Groq API for resume analysis and career guidance.
- **Hosting**: Locally hosted for development; deployable to platforms like Vercel (frontend) and Render (backend).

## Technologies Used
- **Frontend**: React, Vite, Axios, CSS
- **Backend**: FastAPI, PyPDF2, python-docx
- **AI**: Groq API (replaceable with other free-tier APIs like OpenAI or Hugging Face)
- **Rationale**: React + Vite for speed and modern UI, FastAPI for lightweight and fast backend, Python for AI compatibility.

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- Groq API key

### Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   cd frontend