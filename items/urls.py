from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),

    path('buy_order/<int:order_id>/', views.buy_order, name='buy_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]