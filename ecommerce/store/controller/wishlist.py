from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from store.models import Product, Wishlist

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request,'store/wishlist.html',context)
    
def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product Already In Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Product Added To Wishlist"})
            else:
                return JsonResponse({'status':"No Such Porduct Found"})
        else:
            return JsonResponse({'status':"Login To Continue"})
    return redirect(',')

def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status': "Product Removed From Wishlist"})
            else:
                return JsonResponse({'status': "Product Not Find In Wishlist"})
        else:
            return JsonResponse({'status': "Login To Continue"})
    return redirect('/')