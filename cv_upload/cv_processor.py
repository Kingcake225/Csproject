import fitz
import spacy
import re
from typing import Dict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    text = ""
    try:
        # Create a temporary PDF document from the uploaded file
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def structure_cv_data(text: str) -> Dict:
    """Structure CV data by extracting key information"""
    doc = nlp(text)
    
    structured_data = {
        "name": None,
        "email": None,
        "education": [],
        "skills": [],
        "experience": [],
        "years_experience": 0
    }
    
    # Extract email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        structured_data["email"] = email_match.group(0)
    
    # Extract name (usually first PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not structured_data["name"]:
            structured_data["name"] = ent.text
    
    # Extract education
    education_keywords = ["PhD", "Masters", "Bachelor", "BSc", "MSc", "BA", "MA", "A-Level"]
    for line in text.split('\n'):
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                structured_data["education"].append(line.strip())
    
    # Extract skills
    skill_keywords = [
        "Python", "Java", "JavaScript", "SQL", "Git", "AWS", "Docker",
        "Communication", "Leadership", "Project Management", "Agile",
        "Problem Solving", "Team Work", "Critical Thinking",
        "Public Speaking", "Time Management", "Organization",
        "Computer Science", "Teamwork", "Creative"
    ]
    structured_data["skills"] = [
        skill for skill in skill_keywords 
        if skill.lower() in text.lower()
    ]
    
    # Extract work experience
    experience_section = False
    current_position = []
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if "experience" in line.lower():
            experience_section = True
            continue
            
        if experience_section:
            if line.startswith('•') or line.startswith('-'):
                if current_position:
                    current_position.append(line.strip('•- '))
            elif line:
                if current_position:
                    structured_data["experience"].append(current_position)
                current_position = [line]
    
    if current_position:
        structured_data["experience"].append(current_position)
    
    # Estimate years of experience
    structured_data["years_experience"] = len(structured_data["experience"])
    
    return structured_data
