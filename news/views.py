from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'news/post_list.html', {'posts': posts})

def error(request):
    return render(request, 'news/error.html', {})

def index(request):
    return render(request, 'news/index.html', {})

def contact(request):
    return render(request, 'news/contact.html', {})

def detail_page(request):
    return render(request, 'news/detail-page.html', {})