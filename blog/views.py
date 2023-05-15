from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Article
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.all().order_by('-date')

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

    return render(request, template, context)


@login_required()
def add_article(request):
    """ Add a item """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.slug = slugify(form.instance.title)
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Successfully added article!')
            return redirect(reverse('blog'))
        else:
            messages.error(request, 'Failed to add new article. Please ensure the form is valid.')
    else:
        form = ArticleForm()
        
    template = 'blog/add_article.html'
    context = {
        'form': form,
    }

    return render(request, template, context)