from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category, CategoryAdmin)
