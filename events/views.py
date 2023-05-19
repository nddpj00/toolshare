from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Event
from .models import User
from .forms import EventForm

# Create your views here.
def events_list(request):
    events = Event.objects.all().order_by('-date')

    template = 'events/events_list.html'
    context = {
        'events' : events,
    }

    return render(request, template, context)


def event_detail(request, slug):

    event = get_object_or_404(Event, slug = slug)
    organiser = event.organiser.first_name
    organiser_email = event.organiser.email

    template = 'events/event_detail.html'

    context = {
        'event' : event,
        'organiser' : organiser,
        'email' : organiser_email
    }

    return render(request, template, context)


@login_required()
def add_event(request):
    """ Add an event """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.slug = slugify(form.instance.title)
            form.save()
            messages.success(request, 'Successfully added event!')
            return redirect(reverse('events'))
        else:
            messages.error(request, 'Failed to add new event. Please ensure the form is valid.')
    else:
        form = EventForm()
        
    template = 'events/add_event.html'
    context = {
        'form': form,
    }

    return render(request, template, context)