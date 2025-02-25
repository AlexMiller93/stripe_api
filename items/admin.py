from django.contrib import admin

from .models import Discount, Item, Order, Tax

# Register your models here.
admin.site.register(Item)  
admin.site.register(Order)  
admin.site.register(Discount)   
admin.site.register(Tax)  