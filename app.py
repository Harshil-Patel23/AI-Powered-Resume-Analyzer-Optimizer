from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF for PDF reading
from utils import extract_text_from_pdf,clean_text, extract_skills_by_category, calculate_match_score
from skills_data import skills_data

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads/'
app.config['max_size']=10*1024*1024  #10MB limit

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        # Get job description
        jd_text=request.form['job_description']

        # clean the job description text
        jd_text_cleaned=clean_text(jd_text)

        #Get the pdf name
        resume_file=request.files['pdf_upload']
        if resume_file.filename.endswith('.pdf'):
            filename=secure_filename(resume_file.filename)
            file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            resume_file.save(file_path)
        
        # extract text from the pdf
        resume_text=extract_text_from_pdf(file_path)

        # clean the resume text
        resume_text_cleaned=clean_text(resume_text)

        # extract skills from the resume and job description
        resume_skills=extract_skills_by_category(resume_text_cleaned,skills_data)
        jd_skills=extract_skills_by_category(jd_text_cleaned, skills_data)
        score, details = calculate_match_score(resume_skills, jd_skills)
        return render_template('index.html',
                                   score=score,
                                   details=details,
                                   resume_skills=resume_skills,
                                   jd_skills=jd_skills,
                                   extracted_text=resume_text)

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)