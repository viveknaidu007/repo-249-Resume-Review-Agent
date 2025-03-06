from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ai.resume_analyzer import ResumeAnalyzer
import PyPDF2
from docx import Document  # Updated import for python-docx
import uvicorn  # Still needed for programmatic running
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to extract text from PDF or DOCX
def extract_text(file: UploadFile) -> str:
    filename = file.filename
    if filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith('.docx'):
        doc = Document(file.file)  # Updated to use python-docx
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    # Extract text from the uploaded resume
    resume_text = extract_text(file)

    # Initialize the AI analyzer
    analyzer = ResumeAnalyzer()

    # Analyze the resume and get feedback
    feedback = analyzer.analyze_resume(resume_text)

    return feedback

if __name__ == "__main__":
    # Run the app programmatically using uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)