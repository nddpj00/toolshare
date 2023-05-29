from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Article
from .forms import ArticleForm
from newsletter.models import Newsletter
from newsletter.forms import NewsletterSubscriptionForm

def article_list(request):
    articles = Article.objects.all().order_by('-date')

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "The email address is already subscribed to the newsletter.")
                print("email exists")
            else:
                if request.user.is_authenticated:
                    form.instance.is_registered_already = request.user
                    form.save()
                    messages.success(request, "Thank you. We'll send you a weekly newsletter, keeping you up-to-date with Share Bear.")
                else:
                    form.save()
                    messages.success(request, "Thank you. We'll send you a weekly newsletter, keeping you up-to-date with Share Bear."  )
        else:
            print("something else")
            messages.error(request, "Invalid form data. Please try again.")
    else:
        form = NewsletterSubscriptionForm()

    template = 'blog/article_list.html'
    context = {
        'articles' : articles,
        'form': form
    }

    return render(request, template, context)



def article_detail(request, slug):

    article = get_object_or_404(Article, slug = slug)

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

@login_required()
def edit_article(request, article_id):
    """ Edit a blog article  """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('blog'))

    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated article!')
            return redirect(reverse('detail', kwargs={'slug':article.slug}))
        else:
            messages.error(request, 'Failed to update item. Please ensure the form is valid.')
    else:
        form = ArticleForm(instance=article)
        messages.info(request, f'You are editing {article.title}')

    template = 'blog/edit_article.html'
    context = {
        'form': form,
        'article': article,
    }

    return render(request, template, context)



# @login_required()
# def delete_article(request, article_id):
#     """ Delete a blog article  """
#     if not request.user.is_superuser:
#         messages.error(request, 'Sorry, only site owners can do that.')
#         return redirect(reverse('home'))

#     article = get_object_or_404(Article, pk=article_id)
#     article.delete()
#     messages.success(request, 'Blog deleted!')

#     return redirect(reverse('blog'))

@login_required()
def delete_instance_blog(request, instance_id):
    # Add your cancellation logic here
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('home'))

    article = get_object_or_404(Article, id=instance_id)
    article.delete()
    messages.success(request, 'Article deleted!')

    return redirect('blog')