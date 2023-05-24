from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Event
from .models import User
from .forms import EventForm

# test emails
def send_test_email_attendee(user_first_name, user_email, event_title, event_date, event_location, event_body):
    subject = 'You have been invited to an event'
    template_name = 'events/event_attendee_email.html'
    context = {

        'recipient_name': user_first_name,
        'event_title': event_title,
        'event_date': event_date,
        'event_location': event_location,
        'event_body': event_body,
    }
    message = render_to_string(template_name, context)
    from_email = 'danieljones625@gmail.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


def send_test_email_interested(user_first_name, user_email, event_title, event_date, event_location, event_body):
    subject = 'Thank you for your interest'
    template_name = 'events/event_interested_email.html'
    context = {

        'recipient_name': user_first_name,
        'event_title': event_title,
        'event_date': event_date,
        'event_location': event_location,
        'event_body': event_body,
    }
    message = render_to_string(template_name, context)
    from_email = 'danieljones625@gmail.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


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
    is_attending = event.__class__.objects.filter(attendees=request.user.id).exists()
    print(is_attending)
    template = 'events/event_detail.html'

    context = {
        'event' : event,
        'fname' : organiser_fname,
        'email' : organiser_email,
        'is_attending' : is_attending,
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
        user = request.user
        user_email = request.user.email
        event.attendees.add(user.id)
        event.save()
        messages.success(request, "We've added you to the event list")
        send_test_email_attendee(user.first_name, user.email, event.title, event.date, event.location, event.body)

        events = Event.objects.filter(attendees=user)


        return redirect(reverse('profile'))


    else:
        messages.failure(request, "Oops something went wrong, sorry. Please get in touch")
        return render(request, 'events')


@login_required()
def add_interested(request, event_id):

    # Adds user to attendee list
    if request.method == 'POST':

        event = get_object_or_404(Event, pk=event_id)
        user = request.user
        user_email = request.user.email
        event.interested.add(user.id)
        event.save()
        messages.success(request, "Thanks for your interest")
        send_test_email_interested(user.first_name, user.email, event.title, event.date, event.location, event.body)

        return redirect(reverse('events'))


    else:
        messages.failure(request, "Oops something went wrong, sorry. Please get in touch")
        return render(request, 'events')
