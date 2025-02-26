from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render

from .stripe_handlers import (
    create_checkout_session,
    get_line_items_to_checkout_session, 
    get_discount_from_order, 
    get_tax_from_order,
    create_checkout_session_from_line_items
    )
from .models import Item, Order


def buy_item(request, id: int):
    """ Get session for checkout and return session id. """

    try:
        item = Item.objects.get(id=id)

        # create Stripe Checkout Session
        session = create_checkout_session(item)

        return JsonResponse({'id': session.id})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


def item_detail(request, id: int):
    """ Render item_detail template with item and Stripe Publishable Key. """

    try:
        item = Item.objects.get(id=id)
        return render(request, 'item_detail.html', {
            'item': item,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    

def buy_order(request, order_id: int):
    """ Get session for checkout and return session id. """

    try:
        order = Order.objects.get(id=order_id)

        # Add tax if it exists
        tax_id = get_tax_from_order(order)

        # Get line items from the order to the Checkout Session
        line_items = get_line_items_to_checkout_session(order, tax_id)
    
        # create discount if it exists
        discount_id = get_discount_from_order(order)

        # create Stripe Checkout Session
        session = create_checkout_session_from_line_items(line_items, discount_id)

        return JsonResponse({'id': session.id})
            
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def order_detail(request, order_id: int):
    """ Render order_detail template with order and total price. """
    
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'order_detail.html', {
            'order': order,
            'total_price': order.get_total_price(),
            })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
