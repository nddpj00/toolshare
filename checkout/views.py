from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag',{})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('items'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MxpeKBHuLIEiMgOyFwTYXCSZoHS5wlOunugjhot6RvnoVeY9C3RRHoT1MnQpYVfTEK0LqDGtcn1CRKbvRsy0dUj00j8MW3R7M',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
