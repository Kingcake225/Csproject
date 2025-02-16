from typing import Dict, List, Tuple

# Define job-specific skill requirements and their weights
JOB_REQUIREMENTS = {
    "SE": {  # Software Engineer
        "critical_skills": {
            "Python": 0.9,
            "Java": 0.8,
            "JavaScript": 0.8,
            "SQL": 0.8,
            "Git": 0.7,
            "Data Structures": 0.9,
            "Algorithms": 0.9,
            "Problem-Solving": 0.9,
            "Computer Science": 0.9
        },
        "bonus_skills": {
            "C++": 0.6,
            "Machine Learning": 0.5,
            "Public Speaking": 0.4,
            "Teamwork": 0.6,
            "Time Management": 0.5
        },
        "education_weight": 0.7,
        "experience_weight": 0.3
    },
    "HR": {  # Human Resources
        "critical_skills": {
            "Communication": 0.9,
            "Teamwork": 0.9,
            "Organization": 0.8,
            "Time Management": 0.8,
            "Public Speaking": 0.8
        },
        "bonus_skills": {
            "Problem-Solving": 0.6,
            "Leadership": 0.7
        },
        "education_weight": 0.5,
        "experience_weight": 0.5
    }
}

def calculate_education_score(education_text: str) -> float:
    """Calculate education score based on qualifications"""
    if "A-Level" in education_text:
        return 0.7
    elif "GCSE" in education_text:
        return 0.5
    return 0.3

def calculate_experience_score(years: int) -> float:
    """Calculate experience score based on years"""
    if years >= 3:
        return 1.0
    elif years >= 2:
        return 0.8
    elif years >= 1:
        return 0.6
    return 0.3

def calculate_skills_score(candidate_skills: List[str], job_requirements: Dict) -> float:
    """Calculate skills match score"""
    if not job_requirements:
        return 0.0
        
    critical_skills = job_requirements.get('critical_skills', {})
    bonus_skills = job_requirements.get('bonus_skills', {})
    
    total_possible = sum(critical_skills.values()) + sum(bonus_skills.values())
    if total_possible == 0:
        return 0.0
        
    earned_score = 0
    
    # Check each skill
    candidate_skills_lower = [skill.lower() for skill in candidate_skills]
    
    for skill, weight in critical_skills.items():
        if any(skill.lower() in cand_skill for cand_skill in candidate_skills_lower):
            earned_score += weight
            
    for skill, weight in bonus_skills.items():
        if any(skill.lower() in cand_skill for cand_skill in candidate_skills_lower):
            earned_score += weight
            
    return earned_score / total_possible
