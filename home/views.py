from django.shortcuts import render
from blog.models import Article
from newsletter.models import Newsletter
from newsletter.forms import NewsletterSubscriptionForm
from events.models import Event
from django.contrib import messages

def index(request,):
    """ A view to return the index page and add most recent blogs and events"""
    recentBlogs = Article.objects.exclude(thumb__exact='').order_by('date')[:4]
    recentEvents = Event.objects.exclude(thumb__exact='').order_by('date')[:4]

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

    context = {
        'articles' : recentBlogs,
        'events' : recentEvents,
        'form': form
    }

    return render(request, 'home/index.html', context)