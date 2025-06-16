import streamlit as st
import os
import fitz  # PyMuPDF for PDF reading
from utils import extract_text_from_pdf, clean_text, extract_skills_by_category, calculate_match_score
from skills_data import skills_data

# Set page configuration
st.set_page_config(
    page_title="AI Resume Scanner",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        margin-top:-100px;
        padding: 1rem;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .score-container {
        height:20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .score-text {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    
    .category-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .category-title {
        color: #2E86AB;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .skill-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1565c0;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        border: 1px solid #bbdefb;
    }
    
    .missing-skill {
        background: #ffebee;
        color: #c62828;
        border: 1px solid #ffcdd2;
    }
    
    .matched-skill {
        background: #e8f5e8;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Resume Analyzer & Optimizer</h1>', unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF file", 
            type=['pdf'],
            help="Upload your resume in PDF format (Max 10MB)"
        )
        
        st.subheader("📋 Job Description")
        job_description = st.text_area(
            "Paste the job description here:",
            height=200,
            placeholder="Enter the job description that you want to match your resume against..."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        submit_button = st.button("🚀 ANALYZE RESUME", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Analysis Results")
        results_placeholder = st.empty()
    
    # Process when submit button is clicked
    if submit_button:
        if uploaded_file is not None and job_description.strip():
            with st.spinner("🔍 Analyzing your resume..."):
                try:
                    # Create uploads directory if it doesn't exist
                    os.makedirs("uploads", exist_ok=True)
                    
                    # Save uploaded file
                    file_path = os.path.join("uploads", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(file_path)
                    
                    # Clean texts
                    resume_text_cleaned = clean_text(resume_text)
                    jd_text_cleaned = clean_text(job_description)
                    
                    # Extract skills
                    resume_skills = extract_skills_by_category(resume_text_cleaned, skills_data)
                    jd_skills = extract_skills_by_category(jd_text_cleaned, skills_data)
                    
                    # Calculate match score
                    score, details = calculate_match_score(resume_skills, jd_skills)
                    
                    # Display results in the right column
                    with results_placeholder.container():
                        # Display match score
                        st.markdown(f"""
                        <div class="score-container">
                            <h3 class="score-text" style="    margin-top: -29px;text-align: left; color: white;">Match Score : {score}%</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display detailed analysis
                        st.subheader("📈 Detailed Analysis")
                        
                        st.markdown("**⭐Required Skills:**")

                        # Collect all required skills in one string
                        all_required_skills = ""

                        for category, data in details.items():
                            # st.markdown(f"""
                            # <div class="category-card">
                            #     <div class="category-title">{category.title()}</div>
                            # """, unsafe_allow_html=True)
                            
                            if data['required']:
                                all_required_skills += "".join([f'<span class="skill-tag">{skill}</span>' for skill in data['required']])

                        # Display all skills in the same line
                        st.markdown(all_required_skills, unsafe_allow_html=True)


                        st.markdown("**✅ Matching Skills:**")

                        # Collect all required skills in one string
                        all_matching_skills = ""

                        for category, data in details.items():
                            if data['matched']:
                                all_matching_skills += "".join([f'<span class="skill-tag matched-skill">{skill}</span>' for skill in data['matched']])

                        # Display all skills in the same line
                        st.markdown(all_matching_skills, unsafe_allow_html=True)
                            
                        
                        st.markdown("**❌ Missing Skills:**")

                        # Collect all required skills in one string
                        all_missing_skills = ""

                        for category, data in details.items():
                            if data['missing']:
                                all_missing_skills += "".join([f'<span class="skill-tag missing-skill">{skill}</span>' for skill in data['missing']])

                        # Display all skills in the same line
                        st.markdown(all_missing_skills, unsafe_allow_html=True)
                    
                    # Clean up uploaded file
                    os.remove(file_path)
                    
                    # Success message
                    st.success("✅ Analysis completed successfully!")
                    
                    # Optional: Show extracted text in an expander
                    # with st.expander("📄 View Extracted Resume Text"):
                    #     st.text_area("Extracted Text:", value=resume_text, height=200, disabled=True)
                
                except Exception as e:
                    st.error(f"❌ Error processing your resume: {str(e)}")
                    st.error("Please make sure your PDF is valid and try again.")
        
        elif uploaded_file is None:
            st.warning("⚠️ Please upload a PDF file.")
        elif not job_description.strip():
            st.warning("⚠️ Please enter a job description.")
    
    # Sidebar with additional information
    # with st.sidebar:
    #     st.markdown("## 🛠️ How to Use")
    #     st.markdown("""
    #     1. **Upload Resume**: Upload your resume in PDF format
    #     2. **Job Description**: Paste the job description you want to match against
    #     3. **Analyze**: Click the analyze button to get your match score
    #     4. **Review Results**: Check your match score and missing skills
    #     """)
        
    #     st.markdown("## 📋 Features")
    #     st.markdown("""
    #     - **AI-Powered Analysis**: Advanced text processing
    #     - **Skill Matching**: Categorized skill comparison
    #     - **Match Score**: Percentage-based compatibility
    #     - **Gap Analysis**: Identify missing skills
    #     - **Instant Results**: Fast processing
    #     """)
        
    #     st.markdown("## 💡 Tips")
    #     st.markdown("""
    #     - Use a clean, well-formatted PDF
    #     - Include relevant keywords in your resume
    #     - Update your resume based on missing skills
    #     - Try different job descriptions for comparison
    #     """)

if __name__ == "__main__":
    main()
