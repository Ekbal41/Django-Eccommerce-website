

from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

from products.models import Product, SizeVariant
# Create your views here.
from .models import Cart, Profile, cartItems
from products.models import *


def logout_user(request):
    logout(request)
    return redirect('/')


def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')

#---------------------------------------------------------------
@login_required(login_url='/accounts/login')
def cart(request):
    cart = Cart.objects.get(user=request.user , is_paid=False)
    print(cart)
    cartitems =cartItems.objects.filter(cart = cart)
    if not cartitems.exists():
        cart.coupon = None
        cart.save()
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code = coupon)
        if not  coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon.')
            return HttpResponseRedirect(request.path_info)
        
        
            

        if cart.coupon:
            messages.warning(request, 'Coupon already applied.')
            return HttpResponseRedirect(request.path_info)
        if cart.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, 'Minimum order value not reached.')
            return HttpResponseRedirect(request.path_info)
        
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Givem coupon is expired!.')
            return HttpResponseRedirect(request.path_info)
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, 'Coupon applied succesfuly.')
        return HttpResponseRedirect(request.path_info)
    
    context = {
       
        'cart':  cart,
        'cartitems':cartitems
    }
    return render(request , 'accounts/cart.html',   context)
@login_required(login_url='account/login')
def remove_coupon(request, cuid):
    cart = Cart.objects.get(uid =cuid)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon removed succesfuly.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#----------------------------------------------------------------
@login_required(login_url='/accounts/login')
def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _  = Cart.objects.get_or_create(user=user , is_paid=False)
    cart_item = cartItems.objects.create(cart=cart , prodect=product,)
   
    if variant:
        variant = request.GET.get('variant')
        size = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size
        cart_item.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='/accounts/login')    
def remove_from_cart(request, uid):
    try:
        cart_item = cartItems.objects.get(uid=uid)
        cart_item.delete()
    except cartItems.DoesNotExist:
        print("Item does not exist")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





        