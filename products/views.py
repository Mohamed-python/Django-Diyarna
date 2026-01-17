from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Product

def product_list(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'products/product_list.html', {'products': products})


def donate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/donate.html', {'product': product})