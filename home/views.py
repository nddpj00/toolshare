from django.shortcuts import render
from blog.models import Article
from events.models import Event

def index(request,):
    """ A view to return the index page and add most recent blogs and events"""
    recentBlogs = Article.objects.exclude(thumb__exact='').order_by('-date')[:6]
    recentEvents = Event.objects.exclude(thumb__exact='').order_by('-date')[:6]

    context = {
        'articles' : recentBlogs,
        'events' : recentEvents,
    }

    return render(request, 'home/index.html', context)