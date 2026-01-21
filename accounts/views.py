from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_profile.models import Profile

# from django.utils.translation import gettext as _

# Create your views here.
from news.models import News
from products.models import Product
from donations.models import Case

@login_required
def dashboard(request):
    # profile_info = get_object_or_404(Profile, user=request.user)


    cases = Case.objects.order_by('-created_at')[:6]
    
    # جلب آخر 6 منتجات
    products = Product.objects.order_by('-created_at')[:6]
    
    # جلب آخر 3 أخبار
    news_list = News.objects.order_by('-published_at')[:3]
    
    context = {
        'cases': cases,
        'products': products,
        'news_list': news_list,
    }
    print("User logged in:", request.user.username)

    # return redirect('user_profile:profile')

    return render(request, 'dashboard/dashboard.html', context)




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("POST data:", request.POST)  # للتأكد من البيانات جايه

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print()

            # تأكيد تسجيل الدخول
            if request.user.is_authenticated:
                messages.success(request, f"تم تسجيل الدخول بنجاح: {user.username}")
            else:
                messages.error(request, "حدث خطأ، لم يتم تسجيل الدخول")

            return redirect('accounts:dashboard')
        else:
            messages.error(request, "بيانات الدخول غير صحيحة")

    return render(request, 'login.html')



def logout_get(request):
    logout(request)
    return redirect('accounts:login')  # أو أي صفحة تحبها