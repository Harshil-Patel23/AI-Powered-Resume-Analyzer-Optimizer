import re
import fitz

def extract_text_from_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    text_from_resume = ""
    for i in range(len(doc)):  
        text_from_resume += doc.load_page(i).get_text()
    return text_from_resume

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_skills_by_category(text, skills_data):
    matched_skills = {}
    for category, skills in skills_data.items():
        found = []
        for skill in skills:
            skill_lower = skill.lower()
            if re.search(r'\b' + re.escape(skill_lower) + r'\b', text):
                found.append(skill)
        if found:
            matched_skills[category] = found
    return matched_skills

def calculate_match_score(resume_skills, jd_skills):
    total_required = 0
    total_matched = 0
    detailed_result = {}

    for category in jd_skills:
        jd_category_skills = set(jd_skills[category])
        resume_category_skills = set(resume_skills.get(category, []))
        matched = jd_category_skills & resume_category_skills
        total_required += len(jd_category_skills)
        total_matched += len(matched)
        detailed_result[category] = {
            "required": list(jd_category_skills),
            "matched": list(matched),
            "missing": list(jd_category_skills - resume_category_skills)
        }

    match_score = round((total_matched / total_required) * 100, 2) if total_required > 0 else 0
    return match_score, detailed_result
