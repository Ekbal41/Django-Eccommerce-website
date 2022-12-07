from django.urls import path
from accounts.views import login_page,register_page , activate_email,logout_user
from accounts.views import  add_to_cart,cart, remove_from_cart, remove_coupon
from base.invoice import GeneratePdf

urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('add-to-cart/<uid>/' , add_to_cart , name="add_to_cart"),
   path('cart/' , cart , name="cart"),
   path('remove-from-cart/<uid>/' , remove_from_cart , name="remove_from_cart"),
   path('remove_coupon/<cuid>/' , remove_coupon , name="remove_coupon"),
   path('logout/' , logout_user , name="logout" ),
   path('getinvoice/' , GeneratePdf.as_view() , name="getinvoice" ),
]
