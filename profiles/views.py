from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm
from events.models import Event

from checkout.models import Order

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,'Update failed. Please ensure the form is valid')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    events = Event.objects.filter(attendees=request.user)
    

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'events': events,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required()
def cancel_attendance(request, event_id):

    # Adds user to attendee list
    if request.method == 'POST':

        event = get_object_or_404(Event, pk=event_id)
        user = request.user.id
        event.attendees.remove(user)
        event.save()
        messages.success(request, "We've removed you to the event list")


        return redirect(request.META.get('HTTP_REFERER'))


    else:
        messages.failure(request, "Oops something went wrong, sorry. Please get in touch")
        return render(request, 'events')


