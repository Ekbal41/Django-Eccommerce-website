from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Coupon

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')
    
    def get_cart_items(self):
        return cartItems.objects.filter(cart__user=self.user , cart__is_paid=False).count()
    def __str__(self) -> str:
        return self.user.email
class Cart(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="carts")
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon , on_delete=models.SET_NULL , null=True,related_name="carts" ,  blank=True)
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price =[]
        for cr in cart_items:
            price.append(cr.prodect.price)
            if cr.color_variant:
                color_variant_price = cr.color_variant.price
                price.append(color_variant_price)
            if cr.size_variant:
                size_variant_price = cr.size_variant.price
                price.append(size_variant_price)
        
        if self.coupon:
            if self.coupon.is_expired:
                return sum(price)
            if self.coupon.minimum_amount <= sum(price):
                discount = self.coupon.discount
                t = sum(price) - discount
                    
                return t
        
        return sum(price)
    def get_coupon_discount(self):
        discount_price = 0
        if self.coupon:
            if self.coupon.is_expired:
                discount_price += 0
            if not self.coupon:
                discount_price += 0
            else:
                discount_price += self.coupon.discount
        return discount_price
        
    def get_cart_total_without_dis(self):
        cart_items = self.cart_items.all()
        price =[]
        for cr in cart_items:
            price.append(cr.prodect.price)
            if cr.color_variant:
                color_variant_price = cr.color_variant.price
                price.append(color_variant_price)
            if cr.size_variant:
                size_variant_price = cr.size_variant.price
                price.append(size_variant_price)
        return sum(price)
                
    def __str__(self) -> str:
        return self.user.email
        
class cartItems(BaseModel):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name="cart_items")
    prodect = models.ForeignKey('products.Product' , on_delete=models.CASCADE, related_name="cart_items")
    color_variant = models.ForeignKey('products.ColorVariant' , on_delete=models.SET_NULL , related_name="cart_items" , null=True , blank=True)
    size_variant = models.ForeignKey('products.SizeVariant' , on_delete=models.SET_NULL , related_name="cart_items" , null=True , blank=True)
    
    def get_product_price(self):
        price = [self.prodect.price]
        if self.color_variant:
           color_variant_price = self.color_variant.price
           price.append(color_variant_price)
        if self.size_variant:
           size_variant_price = self.size_variant.price
           price.append(size_variant_price)
        return sum(price)
       
    
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)