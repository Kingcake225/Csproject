from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import CVUploadForm
from .models import CV, Message
from .cv_processor import extract_text_from_pdf, structure_cv_data
from django.http import HttpResponseForbidden

# Helper functions to compare CVs
def compare_education(cv1, cv2):
    # See which person has better education
    level1 = cv1.get_education_level_display()
    level2 = cv2.get_education_level_display()
    if level1 != level2:
        return f"Better degree ({level1} vs {level2})"
    return f"Better grades in {cv1.education_discipline}"

def compare_experience(cv1, cv2):
    # Check who has more experience
    years1 = cv1.structured_data.get('years_experience', 0)
    years2 = cv2.structured_data.get('years_experience', 0)
    extra_years = years1 - years2
    if extra_years > 0:
        return f"{extra_years:.1f} years more experience"
    return "Better quality experience"

def compare_skills(cv1, cv2):
    # Look at what extra skills they have
    skills1 = set(cv1.structured_data.get('skills', []))
    skills2 = set(cv2.structured_data.get('skills', []))
    better_at = skills1 - skills2
    if better_at:
        return f"Knows how to: {', '.join(sorted(better_at)[:3])}"
    return "Better at required skills"

@login_required
def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.status = 'PENDING'
            
            # Extract the important bits from the CV
            pdf_text = extract_text_from_pdf(cv.pdf_file)
            cv.structured_data = structure_cv_data(pdf_text)
            cv.save()
            
            # Work out how good they are for the job
            cv.update_ranking()
            messages.success(request, 'Your CV has been uploaded successfully!')
            return redirect('profile')
    else:
        form = CVUploadForm()
    return render(request, 'cv_upload/upload.html', {'form': form})

@login_required
def messages_view(request):
    user_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'cv_upload/messages.html', {'messages': user_messages})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Get all CVs first
    cvs = CV.objects.all()
    
    # Group CVs by position and calculate their scores
    positions = {}
    for cv in cvs:
        position = cv.get_position_display()
        if position not in positions:
            positions[position] = []
        
        # Make sure we have fresh rankings
        cv.update_ranking()
        
        # Get their scores if we've rated them
        scoring_details = None
        if cv.rating is not None and hasattr(cv, 'structured_data'):
            scoring_details = {
                'education': cv.structured_data.get('education_score', 0),
                'experience': cv.structured_data.get('experience_score', 0),
                'skills': cv.structured_data.get('skills_score', 0),
            }
            
            # See how much better they are than the person below them
            if position in positions and positions[position]:
                prev_cv = positions[position][-1]
                if prev_cv.scoring_details:
                    ed_diff = scoring_details['education'] - prev_cv.scoring_details['education']
                    exp_diff = scoring_details['experience'] - prev_cv.scoring_details['experience']
                    sk_diff = scoring_details['skills'] - prev_cv.scoring_details['skills']
                    
                    scoring_details['differences'] = {
                        'education': ed_diff,
                        'education_reason': get_education_comparison(cv, prev_cv) if ed_diff > 0.01 else None,
                        'experience': exp_diff,
                        'experience_reason': get_experience_comparison(cv, prev_cv) if exp_diff > 0.01 else None,
                        'skills': sk_diff,
                        'skills_reason': get_skills_comparison(cv, prev_cv) if sk_diff > 0.01 else None,
                    }
        
        cv.scoring_details = scoring_details
        positions[position].append(cv)
    
    # Sort each position's CVs by their rating
    for position in positions:
        positions[position].sort(key=lambda x: (x.rating if x.rating is not None else -1), reverse=True)
    
    return render(request, 'cv_upload/admin_dashboard.html', {
        'positions': positions,
        'cvs': cvs
    })

@user_passes_test(lambda u: u.is_staff)
def accept_cv(request, cv_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    cv = get_object_or_404(CV, id=cv_id)
    cv.status = 'ACCEPTED'
    cv.save()
    
    Message.objects.create(
        sender=request.user,
        recipient=cv.user,
        subject='CV Accepted',
        content=f'Congratulations! Your CV for the {cv.get_position_display()} position has been accepted.'
    )
    
    messages.success(request, f'CV for {cv.name} has been accepted')
    return redirect('cv_upload:admin_dashboard')

@user_passes_test(lambda u: u.is_staff)
def reject_cv(request, cv_id):
    if request.method != 'POST':
        return HttpResponseForbidden()
    cv = get_object_or_404(CV, id=cv_id)
    cv.status = 'REJECTED'
    cv.save()
    
    Message.objects.create(
        sender=request.user,
        recipient=cv.user,
        subject='CV Status Update',
        content=f'Thank you for your application for the {cv.get_position_display()} position. Unfortunately, we will not be proceeding with your application at this time.'
    )
    
    messages.success(request, f'CV for {cv.name} has been rejected')
    return redirect('cv_upload:admin_dashboard')

@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_all_cvs(request):
    CV.objects.all().delete()
    messages.success(request, 'All CVs have been deleted successfully')
    return redirect('cv_upload:admin_dashboard')

@login_required
@require_POST
def delete_all_messages(request):
    Message.objects.filter(recipient=request.user).delete()
    messages.success(request, 'All messages have been deleted successfully')
    return redirect('cv_upload:messages')

@user_passes_test(lambda u: u.is_staff)
def view_cv_details(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    return render(request, 'cv_upload/cv_details.html', {
        'cv': cv
    })

