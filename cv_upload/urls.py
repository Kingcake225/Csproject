from django.urls import path
from . import views

app_name = 'cv_upload'

urlpatterns = [
    path('upload/', views.upload_cv, name='upload'),
    path('messages/', views.messages_view, name='messages'),
    path('accept-cv/<int:cv_id>/', views.accept_cv, name='accept_cv'),
    path('reject-cv/<int:cv_id>/', views.reject_cv, name='reject_cv'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-all-cvs/', views.delete_all_cvs, name='delete_all_cvs'),
    path('delete-all-messages/', views.delete_all_messages, name='delete_all_messages'),
    path('cv-details/<int:cv_id>/', views.view_cv_details, name='cv_details'),
]
