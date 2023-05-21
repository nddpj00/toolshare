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
    organiser_fname = event.organiser.first_name
    organiser_email = event.organiser.email

    template = 'events/event_detail.html'

    context = {
        'event' : event,
        'fname' : organiser_fname,
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


@login_required()
def edit_event(request, event_id):
    """ Edit an event article  """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('home'))

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated article!')
            return redirect(reverse('event_detail', kwargs={'slug':event.slug}))
        else:
            messages.error(request, 'Failed to update item. Please ensure the form is valid.')
    else:
        form = EventForm(instance=event)
        messages.info(request, f'You are editing {event.title}')

    template = 'events/edit_event.html'
    context = {
        'form': form,
        'event': event,
    }

    return render(request, template, context)


@login_required()
def delete_instance_event(request, instance_id):
    # Add your cancellation logic here
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site owners can do that.')
        return redirect(reverse('home'))

    event = get_object_or_404(Event, id=instance_id)
    event.delete()
    messages.success(request, 'Event deleted!')

    return redirect('events')


@login_required()
def add_attendee(request, event_id):

    # Adds user to attendee list
    if request.method == 'POST':

        event = get_object_or_404(Event, pk=event_id)
        user = request.user.id
        event.attendees.add(user)
        event.save()
        messages.success(request, "We've added you to the event list")

        events = Event.objects.filter(attendees=user)


        return redirect(reverse('profile'))


    else:
        messages.failure(request, "Oops something went wrong, sorry. Please get in touch")
        return render(request, 'events')
