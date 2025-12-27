import streamlit as st
import zipfile
import io
import os
import pandas as pd
from typing import List, Optional

from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# ==================================================
# ENV + STREAMLIT CONFIG
# ==================================================
load_dotenv()
st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="centered")

# ==================================================
# UI / UX STYLES + ANIMATIONS
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8f9ff, #eef2ff);
    font-family: 'Segoe UI', sans-serif;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
.card {
    background: white;
    padding: 1.6rem;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    animation: fadeSlide 0.6s ease forwards;
    margin-bottom: 1.5rem;
}
.title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    color: #555;
    margin-bottom: 1.2rem;
}
.stDownloadButton button, .stButton button {
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# API KEY CHECK
# ==================================================
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ GOOGLE_API_KEY not found. Check your .env file.")
    st.stop()

# ==================================================
# LLM
# ==================================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ==================================================
# SCHEMA (TOLERANT + STRICT)
# ==================================================
class ResumeSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    experience_summary: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

parser = PydanticOutputParser(pydantic_object=ResumeSchema)

# ==================================================
# PROMPT (STRICT JSON DISCIPLINE)
# ==================================================
prompt = ChatPromptTemplate.from_template("""
You are an automated resume parsing system.

Return ONLY valid JSON that strictly follows the schema.
Rules:
- If a field is missing, use null
- Skills MUST be a list of strings
- Do NOT add extra keys
- Do NOT add explanations

Resume Text:
{resume_text}

{format_instructions}
""")

# ==================================================
# FILE READERS
# ==================================================
def read_pdf(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

# ==================================================
# RESUME PARSER (ROBUST)
# ==================================================
def parse_resume(text):
    MAX_CHARS = 6000
    text = text[:MAX_CHARS]

    chain = prompt | llm | parser
    return chain.invoke({
        "resume_text": text,
        "format_instructions": parser.get_format_instructions()
    })

# ==================================================
# UI
# ==================================================
st.markdown('<div class="title">AI Resume Parsing System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a ZIP of resumes and download structured CSV instantly</div>', unsafe_allow_html=True)

uploaded_zip = st.file_uploader("📂 Upload ZIP (PDF / DOCX)", type=["zip"])

if uploaded_zip:
    results = []
    failed = 0

    with st.spinner("🤖 Reading and parsing resumes..."):
        with zipfile.ZipFile(uploaded_zip) as zip_ref:
            for file_name in zip_ref.namelist():

                if "__MACOSX" in file_name:
                    continue

                if not (file_name.endswith(".pdf") or file_name.endswith(".docx")):
                    continue

                with zip_ref.open(file_name) as file:
                    try:
                        text = (
                            read_pdf(io.BytesIO(file.read()))
                            if file_name.endswith(".pdf")
                            else read_docx(io.BytesIO(file.read()))
                        )

                        if not text or len(text.strip()) < 50:
                            failed += 1
                            continue

                        parsed = parse_resume(text)
                        row = parsed.model_dump()
                        row["file_name"] = file_name
                        results.append(row)

                    except Exception as e:
                        failed += 1
                        st.warning(f"⚠️ Failed parsing {file_name}")
                        st.code(str(e))

    if results:
        df = pd.DataFrame(results)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.success(f"✅ Parsed {len(results)} resumes | ❌ Failed {failed}")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            csv,
            "parsed_resumes.csv",
            "text/csv"
        )
        st.markdown('</div>', unsafe_allow_html=True)
