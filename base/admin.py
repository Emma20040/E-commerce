from django.contrib import admin
from .models import Product, OrderItem, Customer, ItemType, Profile


admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(ItemType)
admin.site.register(Profile)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('image','name', 'price', 'description')

# Register your models here.
