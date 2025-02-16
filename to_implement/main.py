import fitz  # PyMuPDF for PDF text extraction
import spacy
import json
import re
import anthropic
import private_apikey
claude = anthropic.Anthropic(api_key=private_apikey.CLAUDE_API_KEY)

# Load the NLP model (use a pre-trained model with NER capabilities)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def structure_cv_data(text):
    """Structures CV data by extracting key entities such as name, email, and address from the text."""
    doc = nlp(text)
    structured_data = {
        "name": None,
        "email": None,
        "address": None,
        "work_experience": [],
        "skills": []
    }
    
    # Extract name and address
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not structured_data["name"]:
            structured_data["name"] = ent.text
    
    # Look for Bristol postcode in text. This is the only way I can think of to extract a correct address. Downside is that it will only work for Bristol poscodes and sometimes it still extracts the wrong data which isn't an address.
    postcode_match = re.search(r'BS\d+\s*\w*', text)
    if postcode_match:
        # Search around postcode for full address
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if postcode_match.group() in line:
                # Take the line with postcode and previous line if it exists
                address_parts = []
                if i > 0:
                    prev_line = lines[i-1].strip()
                    if prev_line:
                        address_parts.append(prev_line)
                address_parts.append(line.strip())
                structured_data["address"] = ", ".join(address_parts)
                break
    
    # Extract email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        structured_data["email"] = email_match.group(0)
    
    # Extract work experience using Claude API
    work_experience_prompt = f"""Extract work experience from this resume text. Format each job exactly as:
    Job Title, Company (dates)
    • Bullet point 1
    • Bullet point 2
    etc.
    
    Resume text to extract from:
    {text}"""
    
    try:
        response = claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.3,
            system="You are a helpful assistant that extracts work experience from resume text. Only output the formatted work experience, nothing else.",
            messages=[
                {"role": "user", "content": work_experience_prompt}
            ]
        )
        
        # Parse the response into individual entries
        work_exp_text = response.content[0].text
        entries = work_exp_text.strip().split('\n')
        
        current_job = []
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
                
            if entry.startswith('•'):
                # Add bullet point detail
                current_job.append(entry.strip('• ').strip())
            else:
                # New job title found
                if current_job:
                    # Push the current job to work_experience if exists
                    structured_data["work_experience"].append(current_job)
                    current_job = []
                current_job.append(entry)
                
        # Add final job if exists
        if current_job:
            structured_data["work_experience"].append(current_job)
            
    except Exception as e:
        print(f"Error extracting work experience: {str(e)}")
        structured_data["work_experience"] = []
    
    # Extract skills
    skills_keywords = ["Python", "Java", "C++", "JavaScript", "SQL", "Git", "Data Structures", "Algorithms", "AWS", "Docker", "Kubernetes", "Agile Development", "Microservices", "Machine Learning", "REST APIs",
    "Talent Acquisition", "Employee Relations", "Onboarding", "HR Policies", "Payroll Processing", "Performance Management", "Conflict Resolution", "ATS (Applicant Tracking System)", "Benefits Administration", "Training & Development", "Labor Laws", "Compensation & Benefits", "HR Analytics", "Workplace Diversity", "Organizational Development",
    "Customer Support", "CRM Software (Salesforce, Zendesk)", "Communication Skills", "Problem-Solving", "Conflict Resolution", "Multitasking", "Active Listening", "Product Knowledge", "Upselling & Cross-Selling", "Call Center Operations", "Email Etiquette", "Time Management", "Customer Satisfaction",
    "Social Media Strategy", "Content Creation", "SEO Optimization", "Facebook Ads", "Instagram Marketing", "Twitter Analytics", "Google Analytics", "Brand Management", "Influencer Marketing", "Hashtag Strategy", "Copywriting", "Community Engagement", "Video Editing", "Canva / Photoshop", "Digital Advertising",
    "Regulatory Compliance", "Risk Assessment", "Internal Audits", "Financial Regulations (SOX, GDPR, HIPAA)", "AML (Anti-Money Laundering)", "Fraud Detection", "Policy Development", "Data Privacy", "Ethics & Integrity", "Legal Research", "Due Diligence", "Process Improvement", "Compliance Monitoring", "Enterprise Risk Management", "SEC Reporting", "Photoshop", "Public Speaking", "Creative writing"]
    structured_data["skills"] = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    
    return structured_data

def save_to_json(data, output_path):
    """Saves structured data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    pdf_path = "Sean.pdf"  # Change to your PDF file path
    output_json = "structured_resume.json"
    
    text = extract_text_from_pdf(pdf_path)
    structured_data = structure_cv_data(text)
    save_to_json(structured_data, output_json)
    
    print("Structured data extracted and saved to", output_json)
