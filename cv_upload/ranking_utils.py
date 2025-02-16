from typing import Dict
from .ranking import (
    calculate_education_score,
    calculate_experience_score,
    calculate_skills_score,
    JOB_REQUIREMENTS
)

def get_position_requirements(position: str) -> Dict:
    """Map CV upload position choices to ranking requirements"""
    position_map = {
        'SE': 'Software Engineer',
        'HR': 'Human Resources',
        'CSR': 'Client Services Representative',
        'SMM': 'Social Media Manager',
        'CA': 'Compliance Analyst'
    }
    full_position = position_map.get(position)
    return JOB_REQUIREMENTS.get(full_position, {})

def rank_candidate(cv_data: Dict, position: str) -> Dict:
    """Calculate ranking scores for a candidate"""
    job_req = get_position_requirements(position)
    if not job_req:
        return {
            'total_score': 0,
            'education_score': 0,
            'experience_score': 0,
            'skills_score': 0
        }
    
    # Calculate individual scores
    education_score = calculate_education_score(
        ' '.join(cv_data.get('education', []))
    )
    experience_score = calculate_experience_score(
        cv_data.get('years_experience', 0)
    )
    skills_score = calculate_skills_score(
        cv_data.get('skills', []),
        job_req
    )
    
    # Calculate weighted total
    total_score = (
        education_score * job_req['education_weight'] +
        experience_score * job_req['experience_weight'] +
        skills_score * (1 - job_req['education_weight'] - job_req['experience_weight'])
    )
    
    return {
        'total_score': round(total_score, 2),
        'education_score': round(education_score, 2),
        'experience_score': round(experience_score, 2),
        'skills_score': round(skills_score, 2)
    }
