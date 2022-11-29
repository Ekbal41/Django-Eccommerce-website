from django.contrib import admin

# Register your models here.
from .models import Profile, cartItems, Cart

admin.site.register(Profile)
admin.site.register(cartItems)
admin.site.register(Cart)
