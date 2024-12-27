import os
import re
from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Load the Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""


def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""


def extract_details(text):
    """Extract email, phone number."""
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.search(r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

    return {
        "Email": email.group(0) if email else "Not Found",
        "Phone": phone.group(0) if phone else "Not Found"
    }


def calculate_similarity(job_desc, resume_text):
    """Calculate similarity score between job description and resume text."""
    job_embedding = model.encode(job_desc, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    similarity = util.cos_sim(job_embedding, resume_embedding).item()
    return round(similarity * 100, 2)


def extract_keywords(text, documents):
    """Extract top keywords based on TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    response = []
    for doc_idx in range(len(documents)):
        doc = tfidf_matrix[doc_idx]
        indices = doc.toarray().argsort()[0][-5:][::-1]  # Top 5 important words
        important_words = [feature_names[i] for i in indices]
        response.append(", ".join(important_words))

    return response


@app.route('/')
def home():
    """Render the main HTML page."""
    return render_template('matchresume.html')


@app.route('/match', methods=['POST'])
def match_resumes():
    """Match resumes with the job description and extract details."""
    job_description_text = request.form.get('job_description_text')
    job_description_file = request.files.get('job_description_file')
    resumes = request.files.getlist('resumes')
    results = []

    if not job_description_text and not job_description_file:
        return render_template('matchresume.html', message="Please provide a job description.")

    # Handle job description (either text or file)
    if job_description_text:
        job_description = job_description_text
    elif job_description_file and allowed_file(job_description_file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_description_file.filename))
        job_description_file.save(file_path)
        if job_description_file.filename.endswith('.pdf'):
            job_description = extract_text_from_pdf(file_path)
        elif job_description_file.filename.endswith('.docx'):
            job_description = extract_text_from_docx(file_path)
        elif job_description_file.filename.endswith('.txt'):
            job_description = extract_text_from_txt(file_path)
    else:
        return render_template('matchresume.html', message="Invalid file format for job description.")

    # Process resumes
    if not resumes:
        return render_template('matchresume.html', message="Please upload at least one resume.")

    documents = [job_description]  # Start with job description as the first document
    for resume in resumes:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume.filename))
        resume.save(file_path)

        # Extract text from resume
        if resume.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif resume.filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        elif resume.filename.endswith('.txt'):
            resume_text = extract_text_from_txt(file_path)
        else:
            continue

        # Add resume text to documents for keyword extraction
        documents.append(resume_text)

        # Extract details and calculate similarity
        details = extract_details(resume_text)
        score = calculate_similarity(job_description, resume_text)

        # Get top keywords for job description and resume
        keywords = extract_keywords(resume_text, documents)

        # Save results (removed Name field)
        results.append({
            "Filename": resume.filename,
            "Email": details["Email"],
            "Phone": details["Phone"],
            "Similarity Score": score,
            "Keywords": keywords[1],  # Keywords for the resume (not job description)
        })

    # Sort by similarity score in descending order
    results.sort(key=lambda x: x["Similarity Score"], reverse=True)

    # Save results to an Excel file
    output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'resume_results.xlsx')
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)  # Removed "Suggested Words"

    return render_template('matchresume.html', results=results, message="Resumes processed successfully!")


@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated Excel file."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)