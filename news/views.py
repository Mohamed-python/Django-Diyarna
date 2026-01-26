from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from django.db.models import F

# Create your views here.

def news_page(request):
    news_list = News.objects.order_by('-published_at')
    return render(request, 'news_list.html', {'news_list': news_list})


def news_detail(request, slug):
    # جلب الخبر حسب الـ slug أو عرض 404 لو مش موجود
    news_item = get_object_or_404(News, slug=slug)


    # اضافه العدد
    key = f'views_count_{news_item.id}'
    if not request.session.get(key):
        News.objects.filter(id=news_item.id).update(
            views_count=F('views_count') + 1
        )
        request.session[key] = True

    
    return render(request, 'news_detail.html', {
        'news': news_item
    })