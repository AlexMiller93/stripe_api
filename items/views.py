from django.conf import settings
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
import stripe

from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return HttpResponse("Hello World!")


def buy_item(request, id: int):
    """ 
        Метод для покупки предмета Item и получить Stripe Session Id для оплаты выбранного предмета
    """
    try:
        item = Item.objects.get(id=id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        return JsonResponse({'id': session.id})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


def item_detail(request, id: int):
    """ 
        Метод для получения HTML страницы для отображения информации выбранном предмете Item.
        По нажатию кнопки Buy происходит запрос на url /buy/{id}, получение session_id 
        и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму 
        
        stripe.redirectToCheckout(sessionId=session_id)

    """
    try:
        item = Item.objects.get(id=id)
        return render(request, 'item_detail.html', {
            'item': item,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
def buy_order(request, order_id: int):
    return HttpResponse(f"Order {order_id} has been successfully processed!")