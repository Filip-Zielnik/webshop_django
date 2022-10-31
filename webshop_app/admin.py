from django.contrib import admin

from .models import Address, Cart, Category, Comment, Order, Product, Profile


class AddressAdmin(admin.ModelAdmin):
    """ Modifies addresses toolbar in Django admin site. """
    list_display = ('profile', 'city', 'country')


class ProductAdmin(admin.ModelAdmin):
    """ Modifies products toolbar in Django admin site. """
    list_display = ('product', 'category', 'price', 'available')
    list_editable = ('available',)


class CartAdmin(admin.ModelAdmin):
    """ Modifies carts toolbar in Django admin site. """
    list_display = ('product', 'quantity', 'user')
    list_editable = ('quantity',)


class CommentAdmin(admin.ModelAdmin):
    """ Modifies comments toolbar in Django admin site. """
    list_display = ('user', 'product')


admin.site.register(Address, AddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Order)
