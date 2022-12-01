from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views.generic import View, TemplateView, DetailView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.models import Cart
from accounts.models import cartItems

from .models import Transaction
from .sslcommerz import sslcommerz_payment_gateway

class IndexView(TemplateView):
    template_name = "home.html"

def PaymentView(request, amount):
    return redirect(sslcommerz_payment_gateway(request, amount))


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutSuccessView(View):
    model = Transaction
    template_name = 'mainsite/carts/checkout-success.html'

    
    def get(self, request, *args, **kwargs):

        # return render(request, self.template_name,{'transaction':transaction})
        return HttpResponse('nothing to see')

    def post(self, request, *args, **kwargs):

        data = self.request.POST
        user = get_object_or_404(User, email=data['value_b'])
        profile = user.profile
        cart = get_object_or_404(Cart, user = user, is_paid=False)
        cartitems =cartItems.objects.filter(cart = cart)
        itemlist = ''
        
        for item in cartitems:
            price = item.prodect.price
            strprice = str(price)
            itemlist += f"Item : {item.prodect.product_name} Price : {strprice}" +'\n'
        try:
            Transaction.objects.create(
                items = itemlist,
                user = user,
                profile = profile,
                name = data['value_a'],
                tran_id=data['tran_id'],
                val_id=data['val_id'],
                amount=data['amount'],
                card_type=data['card_type'],
                card_no=data['card_no'],
                store_amount=data['store_amount'],
                bank_tran_id=data['bank_tran_id'],
                status=data['status'],
                tran_date=data['tran_date'],
                currency=data['currency'],
                card_issuer=data['card_issuer'],
                card_brand=data['card_brand'],
                card_issuer_country=data['card_issuer_country'],
                card_issuer_country_code=data['card_issuer_country_code'],
                verify_sign=data['verify_sign'],
                verify_sign_sha2=data['verify_sign_sha2'],
                currency_rate=data['currency_rate'],
                risk_title=data['risk_title'],
                risk_level=data['risk_level'],

            )
            messages.success(request,'Payment Successfull')
            cart.is_paid = True
            cart.delete()
            
            
        except:
            messages.error(request,'Something bla bla Went Wrong')
        return render(request, 'success.html')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFaildView(View):
    template_name = 'faild.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)