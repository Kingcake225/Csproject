from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from main import extract_text_from_pdf, structure_cv_data
from ranking import rank_candidates, get_job_fit_analysis

def upload_cvs(request):
    if request.method == 'POST' and request.FILES.getlist('files[]'):
        fs = FileSystemStorage()
        files = request.FILES.getlist('files[]')
        job_title = request.POST.get('job_title')
        
        if not job_title:
            return JsonResponse({'error': 'No job title specified'}, status=400)

        cv_data_list = []
        
        for file in files:
            if file.name.endswith('.pdf'):
                # Save file temporarily
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                
                try:
                    # Extract text from PDF
                    text = extract_text_from_pdf(file_path)
                    # Structure the CV data
                    cv_data = structure_cv_data(text)
                    cv_data_list.append(cv_data)
                except Exception as e:
                    # Clean up file
                    fs.delete(filename)
                    return JsonResponse({'error': f'Error processing {file.name}: {str(e)}'}, status=500)
                
                # Clean up file
                fs.delete(filename)
        
        if not cv_data_list:
            return JsonResponse({'error': 'No valid CVs processed'}, status=400)
        
        try:
            # Rank the candidates
            rankings = rank_candidates(cv_data_list, job_title)
            
            # Get detailed job fit analysis for each candidate
            detailed_results = []
            for cv_data in cv_data_list:
                job_fits = get_job_fit_analysis(cv_data)
                detailed_results.append({
                    'name': cv_data.get('name', 'Unknown'),
                    'job_fits': job_fits
                })
            
            return JsonResponse({
                'rankings': rankings,
                'detailed_results': detailed_results
            })
        except Exception as e:
            return JsonResponse({'error': f'Error ranking candidates: {str(e)}'}, status=500)

    return render(request, 'cv_ranker/upload.html')
