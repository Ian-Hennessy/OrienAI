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



def analyze_resume(text):
    prompt = f"""
You are a highly experienced career mentor and recruiter. Your task is to analyze the following resume and provide structured, high-quality feedback that is both informative and encouraging. Your analysis should cover:

Formatting Issues: Identify any layout or design problems that could confuse the reader or detract from the overall presentation.
Missing Key Skills: Point out any important skills or competencies—especially those trending in the job market—that appear to be missing from the resume.
Overall Readability: Evaluate how clearly the resume communicates the candidate’s experience and qualifications.
Areas for Improvement: Suggest specific ways to enhance both the quality and quantity of resume points, with a particular focus on soft skills and experiential highlights.
In your response:

Use a friendly, helpful tone as if you were a mentor speaking directly to the candidate. Use the second-person (e.g., “You have,” “You might consider”).
Pay special attention to any hobbies or interests listed outside of academic or professional contexts. Highlight how these can be used to showcase your unique character and strengths.
Employ the “sandwich method” in your feedback: start with positive comments, follow with constructive suggestions for improvement, and end with encouraging, motivating words.
Conclude your analysis with a brief, uplifting phrase to inspire the candidate to keep refining their resume and to explore the rest of the application features.
Avoid using bold or italics, as these are not represented well in the output text.

Resume:
{text}
"""
    response = openai.ChatCompletion.create(model="gpt-4", 
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    if request.method == "POST":
        resume_file = request.files["resume"]
        text = extract_text_from_pdf(resume_file)
        feedback = analyze_resume(text)
        return jsonify({"feedback": feedback})

    return render_template("index.html")

if __name__ == '__main__':
    # Get the port from environment variable, default to 5000 if not set.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)