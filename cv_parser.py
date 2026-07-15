import pdfplumber
from docx import Document
import os

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif ext in [".docx", ".doc"]:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file type: {ext}")


import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def structure_cv(raw_text: str) -> dict:
    prompt = f"""Extract structured information from this CV/resume text.
Return ONLY valid JSON, no other text, in this exact format:
{{
  "skills": ["skill1", "skill2"],
  "years_experience": <number>,
  "roles": [{{"title": "...", "company": "...", "duration": "..."}}],
  "industries": ["industry1"],
  "education": ["degree, institution"]
}}

CV text:
{raw_text}
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    result_text = response.text.strip()
    if result_text.startswith("```"):
        result_text = result_text.split("```")[1]
        if result_text.startswith("json"):
            result_text = result_text[4:]

    return json.loads(result_text)