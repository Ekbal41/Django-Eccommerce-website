from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def index(request):
   
        
    items =Product.objects.all()
    page_num = request.GET.get('page', 1)
    paginator =Paginator(items, 3)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj' : page_obj}
    
        
    if request.method == 'POST':
        text= request.POST.get('text')
        items = Product.objects.filter(product_name__icontains=text)
        page_num = request.GET.get('page', 1)
        paginator =Paginator(items, 3)
        try:
          page_obj = paginator.page(page_num)
        except PageNotAnInteger:
        # if page is not an integer, deliver the first page
          page_obj = paginator.page(1)
        except EmptyPage:
        # if the page is out of range, deliver the last page
          page_obj = paginator.page(paginator.num_pages)

        context = {'page_obj' : page_obj}   
        
        
    return render(request , 'home/index.html' , context) 
        

    