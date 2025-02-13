from flask import Flask, render_template, jsonify, request
import openai
from dotenv import load_dotenv
import pdfminer.high_level
import os
import docx
load_dotenv()
openai.api_key = os.getenv("OPENAIKEY")
app = Flask(__name__)



def extract_text_from_pdf(pdf_file) -> str:
    return pdfminer.high_level.extract_text(pdf_file.stream)

def extract_text_from_docx(docx_file) -> str:
    text = ""
    doc = docx.Document(docx_file.stream)
    for para in doc.paragraphs:
        text += para
    return text 



def analyze_resume_with_specs(text, specs):
    prompt = f"""
You are a highly experienced career mentor and recruiter. Your task is to analyze the following resume and provide structured, high-quality feedback that is both informative and encouraging. Your analysis should cover:

Formatting Issues: Identify any layout or design problems that could confuse the reader or detract from the overall presentation.
Missing Key Skills: Point out any important skills or competencies—especially those trending in t