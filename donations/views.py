from django.shortcuts import render, get_object_or_404, redirect
from .models import Case, Donation
from .forms import DonationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

######################################
# Create your views here.
def donations_list(request):
    cases = Case.objects.all()  # جلب كل الحالات
    return render(request, 'donations/donations_all.html', {'cases': cases})

# def hi(request):
#     cases = Case.objects.all()  # جلب كل الحالات
#     return render(request, 'donations/hi.html', {'cases': cases})




@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        cart_data = request.POST.get('cart_data')

        errors = []

        # فلديشن الاسم
        if not name:
            errors.append("الرجاء إدخال الاسم")

        # فلديشن البريد الإلكتروني
        if not email:
            errors.append("الرجاء إدخال البريد الإلكتروني")
        elif '@' not in email:
            errors.append("الرجاء إدخال بريد إلكتروني صالح")

        #
        if not phone:
            errors.append("الرجاء إدخال رقم الهاتف")
        elif not phone.isdigit() or not (8 <= len(phone) <= 15):
            errors.append("الرجاء إدخال رقم هاتف صالح")

        # فلديشن السلة
        cart_items = json.loads(cart_data or '[]')
        if not cart_items:
            errors.append("السلة فارغة، لا يمكن إتمام الدفع")




        if errors:
            # لو فيه أخطاء، رجع الصفحة مع الأخطاء
            return render(request, 'checkout/checkout.html', {
                'errors': errors,
                'name': name,
                'email': email,
                'phone': phone,
                'cart_items': cart_items
            })

        # حساب الإجمالي
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        print(f"cart_items: {cart_items}")
        # هنا لو الدفع تم، خلي checkout_status=True
        checkout_status = True

        return render(request, 'checkout/checkout_success.html', {
            'name': name,
            'total': total,
            'checkout_status': checkout_status
        })
    
    return render(request, 'checkout/checkout.html')


def donate(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.case = case
            donation.save()

            # نروح على صفحة اختيار الدفع
            return redirect('payment', donation_id=donation.id)
    else:
        form = DonationForm()

    return render(request, 'donations/donate.html', {
        'case': case,
        'form': form
    })






# 
def payment(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        
        # حفظ في الداتا بيز
        donation.payment_method = method
        donation.is_paid = True  # مؤقتًا
        donation.save()



        ################
        print(f"payment_method: {method}")

        # return redirect('hi')


    return render(request, 'donations/payment.html', {
        'donation': donation
    })



