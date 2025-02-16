from django.urls import path
from . import views

app_name = 'cv_ranker'

urlpatterns = [
    path('', views.upload_cvs, name='upload_cvs'),
]
