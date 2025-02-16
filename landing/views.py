from django.shortcuts import render
from django.http import HttpResponse

# Import Models / Database tables
from .models import Post # . at front of models just means the current folder.

def home(request):
    return render(request, 'landing/home.html')


def blog(request):
    context = { # any data to be passed to page is put in this dictionary
        'title': 'Loose Change - Blog',
        'posts': Post.objects.all()
    }
    return render(request, 'landing/blog.html', context)