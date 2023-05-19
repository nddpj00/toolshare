from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Event

# Create your views here.
def events_list(request):
    events = Event.objects.all().order_by('-date')

    template = 'events/events_list.html'
    context = {
        'events' : events,
    }

    return render(request, template, context)