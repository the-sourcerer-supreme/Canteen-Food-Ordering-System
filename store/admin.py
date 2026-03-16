from django.contrib import admin
from .models import *
from .models import Order
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Show description in admin panel
    search_fields = ('name',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Order)