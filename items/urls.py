from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('buy/<int:order_id>/', views.buy_order, name='buy_order'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
]