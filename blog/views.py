from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all().order_by('date')

    template = 'blog/article_list.html'
    context = {
        'articles' : articles,
    }

    return render(request, template, context)



def article_detail(request, slug):
    article = Article.objects.get(slug = slug)

    template = 'blog/article_detail.html'

    context = {
        'article' : article
    }

    return render(request, template, context )