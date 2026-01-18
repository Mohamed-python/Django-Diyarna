from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from donations.models import Case
from products.models import Product
from news.models import News

# test
def test(request):
    cases = Case.objects.all()  # جلب كل الحالات
    products = Product.objects.all()  # جلب كل المنتجات
    return render(request, "home/test.html" , {'cases': cases, 'products':products})



def home(request):
    cases = Case.objects.order_by('-created_at')[:6]  # جلب كل الحالات
    products = Product.objects.order_by('-created_at')[:6]  # جلب كل المنتجات
    news_list = News.objects.order_by('-published_at')[:2] # جلب الاخبار
    return render(request, "home/home.html" , {'cases': cases, 'products':products, 'news_list':news_list})


def about(request):
    #about.html
    return render(request, "about/about.html")


