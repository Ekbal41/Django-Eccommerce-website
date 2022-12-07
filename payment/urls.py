
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "payment"

urlpatterns = [

    path('', IndexView.as_view(), name='home'),
    path('payment/<int:amount>', login_required(PaymentView), name='payment'),
    path('payment/success', CheckoutSuccessView.as_view(), name='success'),
    path('payment/faild', CheckoutFaildView.as_view(), name='faild'),

]