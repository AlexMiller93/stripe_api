# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World!")


def buy_item(request, id: int):
    """ 
        Метод для покупки предмета Item и получить Stripe Session Id для оплаты выбранного предмета
    """
    pass


def item_detail(request, id: int):
    """ 
        Метод для получения HTML страницы для отображения информации выбранном предмете Item.
        По нажатию кнопки Buy происходит запрос на url /buy/{id}, получение session_id 
        и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму 
        
        stripe.redirectToCheckout(sessionId=session_id)

    """
    pass