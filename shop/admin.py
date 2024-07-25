# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from django.contrib import admin
from .models import Category, Product, Order, OrderProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')
