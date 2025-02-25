from django.conf import settings
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
import stripe

from .models import Item, Order

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
    try:
        order = Order.objects.get(id=order_id)
        items = order.items.all()

        # Add tax if it exists
        tax_id = None
        if order.tax:
            tax = stripe.TaxRate.create(
                display_name=order.tax.name,
                description='Sales Tax',
                percentage=float(order.tax.percentage),
                inclusive=False,
            )

            tax_id = tax.id

        # Add items to the order to the Checkout Session
        line_items = []
        for item in items:
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }

            # add tax to the line item if it exists
            if tax_id:
                line_item['tax_rates'] = [tax_id]
            line_items.append(line_item)

        # create discount if it exists
        discount_id = None
        if order.discount:
            coupon = stripe.Coupon.create(
                name=order.discount.name,
                amount_off=int(order.discount.percentage * 100),
                currency='usd',
            )

            discount_id = coupon.id

        # create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            discounts=[{'coupon': discount_id}] if discount_id else None,
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel'
        )

        return JsonResponse({'id': session.id})
            
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def order_detail(request, order_id: int):
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'order_detail.html', {
            'order': order,
            'total_price': order.get_total_price(),
            })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

def test_buy_order(request, order_id: int):
    # if or
    try:
        order = Order.objects.get(id=order_id)
        if order is not None:
            return HttpResponse(f"Order {order_id} has been successfully processed!")
    except Order.DoesNotExist:
        return HttpResponse(f"Oops! ... Order {order_id} no one booked!")