from django.contrib import admin
from .models import Product, Cart, CartItem

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'price')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)
    fields = ('product', 'quantity', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price', 'created_at')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'get_total_price', 'added_at')
    list_filter = ('cart', 'added_at')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('added_at',)

    def get_total_price(self, obj):
        return f"KSh {obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'