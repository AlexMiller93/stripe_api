import decimal
from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.percentage} %"


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.percentage} %"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at  = models.DateTimeField(auto_now_add=True)

    discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)
    
    tax = models.ForeignKey(
        Tax, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)


    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
    
        if self.discount is not None:
            total -= (self.discount.percentage / 100) * total

        if self.tax is not None:
            total += (self.tax.percentage / 100) * total
        
        return total.quantize(decimal.Decimal('0.01'))  # rounding to two decimal places

    def __str__(self):
        return f"Order #{self.id} - {self.created_at.strftime('%m-%d')}"
    