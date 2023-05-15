from django.shortcuts import render
from blog.models import Article

def index(request,):
    """ A view to return the index page and add 4 most recent blogs"""
    recentBlogs = Article.objects.exclude(thumb__exact='').order_by('-date')[:6]

    context = {
        'articles' : recentBlogs,
    }

    return render(request, 'home/index.html', context)