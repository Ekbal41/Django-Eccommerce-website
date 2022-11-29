
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from accounts.models import cartItems
from products.models import SizeVariant
from products.models import Product

from accounts.models import Cart




def get_product(request , slug):
    
    try:
        product = Product.objects.get(slug =slug)
        context = { "product" : product}
        if request.GET.get('size'):
          size = request.GET.get('size')
          price = product.get_product_price_by_size(size)
          print(price)
          context['selected_size'] = size
          context['updated_price'] = price
        

    except Exception as e:
        print(e)
    return render(request  , 'product/product.html' , context = context)

