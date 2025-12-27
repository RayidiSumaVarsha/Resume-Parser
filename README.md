# AI-Powered Resume Analyzer & CSV Generator using LangChain

AI-Powered Resume Analyzer is an intelligent application designed to **automate resume analysis and structured data extraction** for recruiters and HR teams.  
The system processes multiple resumes at once, extracts key information using Large Language Models (LLMs), and generates a **downloadable CSV file** for easy filtering and analysis.

This project is built using **Streamlit** for the user interface and **LangChain** for LLM orchestration, prompt templates, and structured output parsing.

---

## 🚀 Project Overview

Recruiters and HR professionals often receive resumes in bulk, usually as **ZIP files** containing multiple resumes in **PDF or DOCX formats**.  
Manually reviewing each resume and extracting important details is:

- Time-consuming  
- Repetitive  
- Error-prone  
- Inconsistent due to varied resume formats  

This project solves that problem by using **LLM-powered automation** to convert unstructured resume content into **structured CSV data**.

---

## 🎯 What This System Does

The application performs the following tasks:

- Accepts a **ZIP file** containing multiple resumes  
- Automatically reads and processes each resume  
- Extracts structured information using LLMs  
- Enforces a fixed schema for consistency  
- Aggregates all extracted data into a **CSV file**  
- Allows users to **download the CSV directly** from the Streamlit app  

---

## ❗ Problem Statement

- HR teams struggle to analyze large volumes of resumes efficiently  
- Resume formats vary widely (PDF, DOCX, layouts, fonts)  
- Manual extraction of skills, links, and summaries is inconsistent  
- Lack of structured output makes filtering and analysis difficult  

---

## 💡 Solution Approach

This project implements an **LLM-powered resume processing pipeline** using LangChain:

1. Reads resumes from a ZIP file  
2. Extracts raw text from PDF and DOCX resumes  
3. Uses **Prompt Templates** to guide the LLM  
4. Converts unstructured resume text into structured data  
5. Enforces a fixed schema using **TypedDict Output Parser**  
6. Aggregates structured data from all resumes  
7. Generates a consolidated **CSV file**  

---

## 🧠 Key Features

- Bulk resume processing via ZIP upload  
- Supports multiple resume formats (PDF, DOCX)  
- Structured information extraction using LLMs  
- Schema-enforced output for consistency  
- CSV generation for easy analysis  
- Downloadable CSV file from the UI  
- Simple and clean Streamlit interface  

---

## 🏗️ Technical Architecture

### 🧠 Backend Logic
- **LangChain**
  - Prompt Templates
  - Structured Output Parsers (TypedDict)
  - LLM-based information extraction
- Resume text extraction logic (PDF/DOCX)

### 🖥️ Frontend
- **Streamlit**
  - ZIP file upload interface
  - Processing trigger
  - CSV download button

---

## 🛠️ Tech Stack

| Component | Technology |
|--------|-----------|
| Frontend | Streamlit |
| LLM Orchestration | LangChain |
| Prompt Engineering | LangChain Prompt Templates |
| Output Parsing | TypedDict Output Parser |
| File Handling | ZIP, PDF, DOCX |
| Output Format | CSV |

---

## 📥 Input & Output

### Input
- ZIP file containing multiple resumes  
- Supported formats:
  - PDF
  - DOCX  

### Output
- Single **CSV file**
- Each row represents one resume
- Structured and consistent fields for analysis

---

## 📚 Expected Learning Outcomes

By completing this project, learners will gain hands-on experience with:

- Automating document analysis using LLMs  
- Resume parsing and information extraction  
- Prompt engineering for structured outputs  
- Using LangChain output parsers  
- Building data-processing pipelines  
- Creating Streamlit applications for real-world use cases  

---

## ▶️ How to Run the Project

```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd <project-folder>

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
