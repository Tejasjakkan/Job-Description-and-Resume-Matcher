# Job Description and Resume Matcher

## Overview
The Job Description and Resume Matcher is a web-based application designed to automate the recruitment process by analyzing job descriptions and resumes. It uses Natural Language Processing (NLP) techniques to match resumes with job descriptions based on semantic similarity, while also extracting key details such as email addresses, phone numbers, and important keywords.

This solution is ideal for organizations looking to streamline their hiring process, reduce manual effort, and improve candidate selection accuracy.

---

## Features
- **Upload Support**: Supports PDF, DOCX, and TXT formats for job descriptions and resumes.
- **Semantic Matching**: Calculates a similarity score using Sentence-BERT to determine how well a resume matches a job description.
- **Keyword Extraction**: Extracts important keywords from resumes and job descriptions using TF-IDF.
- **Candidate Details**: Extracts email addresses and phone numbers from resumes.
- **Results Download**: Outputs results to an Excel file with matched resumes, similarity scores, and extracted details.
- **User-Friendly Interface**: Built using Flask and Bootstrap for ease of use.

---

## Technologies Used
- **Frontend**:
  - HTML5, CSS3, Bootstrap
- **Backend**:
  - Python, Flask
  - Libraries: PyPDF2, python-docx, SentenceTransformer, sklearn, pandas
- **NLP Model**:
  - Sentence-BERT (`all-MiniLM-L6-v2`)
- **Data Processing**:
  - TF-IDF for keyword extraction
  - Cosine similarity for matching resumes and job descriptions

---

## Installation and Setup

### Prerequisites
1. Python 3.8 or higher
2. pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd job-description-resume-matcher
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

1. **Upload Job Description**:
   - Paste text into the provided text area OR upload a job description file (PDF, DOCX, or TXT).

2. **Upload Resumes**:
   - Select multiple resume files (PDF, DOCX, or TXT).

3. **Submit for Matching**:
   - Click the "Match Resumes" button to process the data.

4. **View Results**:
   - The matched resumes are displayed with their similarity scores, email addresses, phone numbers, and keywords.

5. **Download Results**:
   - Click the "Download Results" button to save the output as an Excel file.

---

## Project Workflow

1. **Input Data**:
   - Job description and resumes are uploaded via the web interface.

2. **Text Extraction**:
   - Extracts text from uploaded PDF, DOCX, and TXT files using PyPDF2 and python-docx.

3. **Semantic Analysis**:
   - Encodes job description and resume text into vector embeddings using Sentence-BERT.
   - Calculates semantic similarity using cosine similarity.

4. **Keyword Extraction**:
   - Applies TF-IDF to extract top keywords from resumes.

5. **Output Results**:
   - Generates an Excel file containing filename, email, phone, similarity score, and keywords.

---

## Output Example
| Filename            | Email                | Phone         | Similarity Score | Keywords                     |
|---------------------|----------------------|---------------|------------------|------------------------------|
| resume1.pdf         | example@gmail.com   | 1234567890    | 85.5%            | Python, Machine Learning     |
| resume2.docx        | candidate@mail.com  | Not Found     | 78.2%            | Data Analysis, SQL          |

---

## Future Enhancements
- **Real-Time Analytics**:
  - Add features to visualize hiring trends and candidate engagement metrics.
- **Advanced Parsing**:
  - Improve parsing for diverse resume formats.
- **Cloud Deployment**:
  - Deploy the application on AWS or Azure for better scalability and availability.
- **Integration with ATS**:
  - Integrate the application with existing Applicant Tracking Systems (ATS).

---

## Contact
For questions, feedback, or contributions, please contact:
- **Name**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile]

