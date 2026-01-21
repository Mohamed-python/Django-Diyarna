from django.shortcuts import render, redirect
from django.contrib import messages
# from django.urls import reverse

# Create your views here.
from products.models import Product
from news.models import News
import json
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType

from donations.models import Case

from collections import defaultdict
from django.db.models import Sum
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
##################################################
##################################################


# test
def test(request):
    cases = Case.objects.all()  # جلب كل الحالات
    products = Product.objects.all()  # جلب كل المنتجات
    return render(request, "home/test.html" , {'cases': cases, 'products':products})


def home(request):

    #########################################
    #########################################
    cases = Case.objects.order_by('-created_at')[:6]  # جلب كل الحالات
    products = Product.objects.order_by('-created_at')[:6]  # جلب كل المنتجات
    news_list = News.objects.order_by('-published_at')[:3] # جلب الاخبار
    return render(request, "home/home.html" , {'cases': cases, 'products':products, 'news_list':news_list})



def board(request):
    return render(request, "board/board.html")

def about(request):
    #about.html
    return render(request, "about/about.html")






