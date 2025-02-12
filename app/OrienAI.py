from flask import Flask, render_template, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import pdfminer.high_level
import os
load_dotenv()

client = OpenAI(os.getenv("OPENAIKEY"))
app = Flask(__name__)

if __name__ == '__main__':
    # Get the port from environment variable, default to 5000 if not set.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# OpenAI API Key

def extract_text_from_pdf(pdf_file):
    return pdfminer.high_level.extract_text(pdf_file.stream)

def analyze_resume(text):
    prompt = f"""
You are a highly experienced career mentor and recruiter. Your task is to analyze the following resume and provide structured, high-quality feedback that is both informative and encouraging. Your analysis should cover:

Formatting Issues: Identify any layout or design problems that could confuse the reader or detract from the overall presentation.
Missing Key Skills: Point out any important skills or competencies—especially those trending in