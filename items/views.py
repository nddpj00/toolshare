from django.shortcuts import render
from . models import Item

def all_items(request):
    """ A view to show all items, including sorting and search queries """

    items = Item.objects.all()

    context = {
        'items' : items,
    }

    return render(request, 'items/items.html', context)