from django.conf import settings
from django.shortcuts import get_object_or_404
from items.models import Item


def bag_contents(request):

    bag_items = []
    total = 0
    item_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        item = get_object_or_404(Item, pk=item_id)
        total += quantity * item.price
        item_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'item': item,
        })

    total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'item_count': item_count,
        'bag': request.session.get('bag', {}),
    }

    return context
