from typing import Any
from django.conf import settings
import stripe

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_tax_from_order(order: Order) -> int:
    """ Returns the tax id from the given order. """
    tax_id = None

    if order:
        tax = stripe.TaxRate.create(
                display_name=order.tax.name,
                description='Sales Tax',
                percentage=float(order.tax.percentage),
                inclusive=False,
            )

        tax_id = tax.id

    return tax_id


def get_discount_from_order(order: Order):
    """ Returns the discount id from the given order."""
    discount_id = None
    if order.discount:
        coupon = stripe.Coupon.create(
            name=order.discount.name,
            amount_off=int(order.discount.percentage * 100),
            currency='usd',
        )

        discount_id = coupon.id

    return discount_id

def create_checkout_session(item: Item) -> list[list]:
    """ Creates and returns a checkout session for the given item."""
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

    return session

def create_checkout_session_from_line_items(line_items : list[dict], discount_id: int) -> list[list]:
    """ Creates and returns a checkout session for the given line_items."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        discounts=[{'coupon': discount_id}] if discount_id else None,
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel'
    )

    return session

def get_line_items_to_checkout_session(order: Order, tax_id: int=None) -> list[dict]:
    """ Returns a list of line items for the given order, including tax if applicable. """
    items = order.items.all()

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

    return line_items
