from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Event
from .models import User
from .forms import EventForm
from newsletter.models import Newsletter
from newsletter.forms import NewsletterSubscriptionForm
from django.template.defaultfilters import linebreaksbr


def send_test_email_attendee(user_first_name, user_email, event_title,
                             event_date, event_location, event_body):
    subject = 'Share Bear Event'
    template_name = 'event_confirmation_emails/event_attendee_email_body.txt'
    print(event_body)

    context = {
        'recipient_name': user_first_name,
        'event_title': event_title.capitalize(),
        'event_date': event_date,
        'event_location': event_location,
        "event_body": event_body,
    }
    message = render_to_string(template_name, context)
    from_email = 'Share Bear Team'
    recipient_list = [user_email]


    send_mail(subject, message, from_email, recipient_list)



def send_test_email_interested(user_first_name, user_email, event_title,
                               event_date, event_location, event_body):
    subject = 'Share Bear Event'
    template_name = 'event_confirmation_emails/event_interested_email_body.txt'
    context = {
        'recipient_name': user_first_name,
        'event_title': event_title.capitalize(),
        'event_date': event_date,
        'event_location': event_location,
        "event_body": event_body,
    }
    message = render_to_string(template_name, context)
    from_email = 'Share Bear Team'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)


def events_list(request):
    events = Event.objects.all().order_by('-date')

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, ('The email address is already'
                               'subscribed to the newsletter.'))
            else:
                if request.user.is_authenticated:
                    form.instance.is_registered_already = request.user
                    form.save()
                    messages.success(request, ('Thank you. We"ll send you a'
                                     'weekly newsletter, keeping you up-to-date'
                                     'with Share Bear.'))
                else:
                    form.save()
                    messages.success(request, ('Thank you. We"ll send you a'
                                     'weekly newsletter, keeping you up-to-date'
                                     'with Share Bear.'))
        else:
            print("something else")
            messages.error(request, "Invalid form data. Please try again.")
    else:
        form = NewsletterSubscriptionForm()

    template = 'events/events_list.html'
    context = {
        'events': events,
        'form': form,
        'on_profile_events_blog_page': True,
    }

    return render(request, template, context)


def event_detail(request, slug):

    event = get_object_or_404(Event, slug=slug)
    organiser_fname = event.organiser.first_name
    organiser_email = event.organiser.email
    is_attending = event.attendees.filter(id=request.user.id).exists()
    template = 'events/event_detail.html'

    context = {
        'event': event,
        'fname': organiser_fname,
        'email': organiser_email,
        'is_attending': is_attending,
        'on_profile_events_blog_page': True,
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
            messages.error(request, ('Failed to add new event. Please ensure the'
                           'form is valid.'))
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
            event = form.save(commit=False)
            event.slug = slugify(event.title)
            form.save()
            messages.success(request, 'Successfully updated article!')
            return redirect(reverse('event_detail',
                            kwargs={'slug': event.slug}))
        else:
            messages.error(request, ('Failed to update item. Please ensure the'
                           'form is valid.'))
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
    event = get_object_or_404(Event, pk=event_id)
    # Adds user to attendee list
    if request.method == 'POST':

        user = request.user
        user_email = request.user.email
        event.attendees.add(user.id)
        event.save()
        messages.success(request, "We've added you to the event list")
        send_test_email_attendee(user.first_name, user.email, event.title,
                                 event.date, event.location, event.body)

        events = Event.objects.filter(attendees=user)

        return redirect(reverse('profile'))

    return redirect(reverse('event_detail', kwargs={'slug': event.slug}))


@login_required()
def add_interested(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Adds user to attendee list
    if request.method == 'POST':

        user = request.user
        user_email = request.user.email
        event.interested.add(user.id)
        event.save()
        messages.success(request, ('Thanks for your interest, we"ll email you'
                         'with some information about the event. Hope to see you'
                         'there!'))
        send_test_email_interested(user.first_name, user.email, event.title,
                                   event.date, event.location, event.body)

        return redirect(reverse('event_detail', kwargs={'slug': event.slug}))

    return redirect(reverse('event_detail', kwargs={'slug': event.slug}))
