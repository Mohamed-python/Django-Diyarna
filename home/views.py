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
from .models import Board
##################################################
from .forms import ContactForm

# test
def test(request):
    cases = Case.objects.all()  # جلب كل الحالات
    products = Product.objects.all()  # جلب كل المنتجات
    return render(request, "home/test.html" , {'cases': cases, 'products':products})


def home(request):
    slides = [
        {
            "image": "home-slider_show/images/slider-1.jpg",
            "title": "Diyarna",
            "subtitle": "The Best Place to Donate",
        },
        {
            "image": "home-slider_show/images/slider-2.jpg",
            "title": "Hope for Tomorrow",
            "subtitle": "Support Those in Need",
        },
        {
            "image": "home-slider_show/images/slider-3.jpg",
            "title": "Hand of Giving",
            "subtitle": "Be Part of the Good",
        },
        {
            "image": "home-slider_show/images/slider-4.jpg",
            "title": "Hope for Tomorrow",
            "subtitle": "Support Those in Need",
        },
    ]
    #########################################
    #########################################
    cases = Case.objects.order_by('-created_at')[:6]  # جلب كل الحالات
    products = Product.objects.order_by('-created_at')[:6]  # جلب كل المنتجات
    news_list = News.objects.order_by('-published_at')[:3] # جلب الاخبار


    ########################

    context={
        'slides':slides,
        'cases': cases, 
        'products':products, 
        'news_list':news_list
        }

    return render(request, "home/home.html" , context=context)


# مجلس الامناء
def board(request):
    board_list = Board.objects.all()
    
    return render(request, "board/board.html", context={'board':board_list})

def about(request):
    #about.html
    return render(request, "about/about.html")








def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/contact_success.html')




