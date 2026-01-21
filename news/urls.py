from django.urls import path, include
from .views import news_page, news_detail
from django.urls import re_path


app_name = 'news'  # مهم جدًا


urlpatterns = [
    # path('', news_page, name='news'),
    re_path(r'^$', news_page, name='news_list'),
    re_path(r'^(?P<slug>[-\w\u0600-\u06FF]+)/$', news_detail, name='news_detail'),
]
