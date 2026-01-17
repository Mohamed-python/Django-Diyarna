from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from donations.models import Case
from products.models import Product


# test
def test(request):
    cases = Case.objects.all()  # جلب كل الحالات
    products = Product.objects.all()  # جلب كل المنتجات
    return render(request, "home/test.html" , {'cases': cases, 'products':products})



def home(request):
    cases = Case.objects.all()  # جلب كل الحالات
    products = Product.objects.all()  # جلب كل المنتجات

    return render(request, "home/home.html" , {'cases': cases, 'products':products})


def about(request):
    #about.html
    return render(request, "about/about.html")


def news_detail(request, id):
    pass