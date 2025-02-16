from typing import Dict, List, Tuple
import json

# Define job-specific skill requirements and their weights
JOB_REQUIREMENTS = {
    "Software Engineer": {
        "critical_skills": {
            "Python": 0.9,
            "Java": 0.8,
            "JavaScript": 0.8,
            "SQL": 0.8,
            "Git": 0.7,
            "Data Structures": 0.9,
            "Algorithms": 0.9,
            "AWS": 0.7,
            "Docker": 0.7,
            "Kubernetes": 0.6,
            "Agile Development": 0.7,
            "Microservices": 0.7,
            "REST APIs": 0.8
        },
        "bonus_skills": {
            "C++": 0.6,
            "Machine Learning": 0.5
        },
        "education_weight": 0.7,
        "experience_weight": 0.8
    },
    "Human Resources": {
        "critical_skills": {
            "Talent Acquisition": 0.9,
            "Employee Relations": 0.8,
            "Onboarding": 0.8,
            "HR Policies": 0.9,
            "Performance Management": 0.8,
            "Conflict Resolution": 0.8,
            "Benefits Administration": 0.7,
            "Labor Laws": 0.9,
            "Compensation & Benefits": 0.8
        },
        "bonus_skills": {
            "HR Analytics": 0.6,
            "ATS (Applicant Tracking System)": 0.7,
            "Workplace Diversity": 0.7,
            "Organizational Development": 0.6,
            "Training & Development": 0.7
        },
        "education_weight": 0.6,
        "experience_weight": 0.7
    },
    "Client Services Representative": {
        "critical_skills": {
            "Customer Support": 0.9,
            "CRM Software (Salesforce, Zendesk)": 0.8,
            "Communication Skills": 0.9,
            "Problem-Solving": 0.8,
            "Conflict Resolution": 0.8,
            "Active Listening": 0.9,
            "Email Etiquette": 0.8,
            "Time Management": 0.7,
            "Customer Satisfaction": 0.9
        },
        "bonus_skills": {
            "Multitasking": 0.7,
            "Product Knowledge": 0.6,
            "Upselling & Cross-Selling": 0.6,
            "Public Speaking": 0.5
        },
        "education_weight": 0.4,
        "experience_weight": 0.8
    },
    "Social Media Manager": {
        "critical_skills": {
            "Social Media Strategy": 0.9,
            "Content Creation": 0.9,
            "SEO Optimization": 0.8,
            "Facebook Ads": 0.8,
            "Instagram Marketing": 0.8,
            "Twitter Analytics": 0.7,
            "Google Analytics": 0.8,
            "Brand Management": 0.8,
            "Copywriting": 0.8,
            "Community Engagement": 0.8
        },
        "bonus_skills": {
            "Influencer Marketing": 0.7,
            "Video Editing": 0.6,
            "Canva / Photoshop": 0.7,
            "Digital Advertising": 0.7,
            "Creative writing": 0.6
        },
        "education_weight": 0.5,
        "experience_weight": 0.7
    },
    "Compliance Analyst": {
        "critical_skills": {
            "Regulatory Compliance": 0.9,
            "Risk Assessment": 0.9,
            "Internal Audits": 0.8,
            "Financial Regulations (SOX, GDPR, HIPAA)": 0.9,
            "AML (Anti-Money Laundering)": 0.8,
            "Policy Development": 0.8,
            "Data Privacy": 0.8,
            "Due Diligence": 0.8,
            "Compliance Monitoring": 0.9
        },
        "bonus_skills": {
            "Fraud Detection": 0.7,
            "Ethics & Integrity": 0.7,
            "Legal Research": 0.6,
            "Process Improvement": 0.6,
            "SEC Reporting": 0.7
        },
        "education_weight": 0.8,
        "experience_weight": 0.7
    }
}

def calculate_education_score(education_level: str) -> float:
    """Calculate education score based on highest level achieved."""
    education_scores = {
        "phd": 1.0,
        "doctorate": 1.0,
        "masters": 0.8,
        "bachelors": 0.6,
        "associate": 0.4,
        "high school": 0.2
    }
    
    # Convert education level to lowercase for matching
    education_level = education_level.lower()
    
    # Look for keywords in the education level
    for level, score in education_scores.items():
        if level in education_level:
            return score
    
    return 0.1  # Default score if no matching education level found

def calculate_experience_score(years_experience: int) -> float:
    """Calculate experience score based on years of experience."""
    if years_experience >= 10:
        return 1.0
    elif years_experience >= 7:
        return 0.8
    elif years_experience >= 5:
        return 0.6
    elif years_experience >= 3:
        return 0.4
    elif years_experience >= 1:
        return 0.2
    else:
        return 0.1

def calculate_skills_score(candidate_skills: List[str], job_requirements: Dict) -> float:
    """
    Calculate skills score based on matching required skills.
    Considers both critical and bonus skills with their respective weights.
    """
    critical_skills = job_requirements['critical_skills']
    bonus_skills = job_requirements['bonus_skills']
    
    total_possible_score = sum(critical_skills.values()) + sum(bonus_skills.values())
    earned_score = 0
    
    # Convert candidate skills to lowercase for matching
    candidate_skills_lower = [skill.lower() for skill in candidate_skills]
    
    # Check critical skills
    for skill, weight in critical_skills.items():
        if any(skill.lower() in candidate_skill for candidate_skill in candidate_skills_lower):
            earned_score += weight
    
    # Check bonus skills
    for skill, weight in bonus_skills.items():
        if any(skill.lower() in candidate_skill for candidate_skill in candidate_skills_lower):
            earned_score += weight
    
    return earned_score / total_possible_score if total_possible_score > 0 else 0

def rank_candidate(cv_data: Dict, job_title: str) -> float:
    """
    Calculate overall ranking score for a candidate based on their CV and the job requirements.
    Returns a score between 0 and 1.
    """
    if job_title not in JOB_REQUIREMENTS:
        raise ValueError(f"Invalid job title: {job_title}")
    
    job_req = JOB_REQUIREMENTS[job_title]
    
    # Calculate individual component scores
    education_score = calculate_education_score(cv_data.get('education', ''))
    experience_score = calculate_experience_score(cv_data.get('years_experience', 0))
    skills_score = calculate_skills_score(cv_data.get('skills', []), job_req)
    
    # Calculate weighted total score
    total_score = (
        education_score * job_req['education_weight'] +
        experience_score * job_req['experience_weight'] +
        skills_score * (1 - job_req['education_weight'] - job_req['experience_weight'])
    )
    
    return round(total_score, 2)

def rank_candidates(cv_list: List[Dict], job_title: str) -> List[Tuple[str, float]]:
    """
    Rank multiple candidates for a specific job position.
    Returns a sorted list of (candidate_name, score) tuples.
    """
    rankings = []
    
    for cv in cv_list:
        try:
            score = rank_candidate(cv, job_title)
            rankings.append((cv.get('name', 'Unknown'), score))
        except ValueError as e:
            print(f"Error ranking candidate: {e}")
            continue
    
    # Sort by score in descending order
    return sorted(rankings, key=lambda x: x[1], reverse=True)

def get_job_fit_analysis(cv_data: Dict) -> Dict[str, float]:
    """
    Analyze how well a candidate fits each available job position.
    Returns a dictionary of job titles and their corresponding fit scores.
    """
    job_fits = {}
    
    for job_title in JOB_REQUIREMENTS.keys():
        try:
            score = rank_candidate(cv_data, job_title)
            job_fits[job_title] = score
        except ValueError as e:
            print(f"Error analyzing job fit: {e}")
            continue
    
    return dict(sorted(job_fits.items(), key=lambda x: x[1], reverse=True))
