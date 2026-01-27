from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from donations.models import Case, Donation
from products.models import Product

from products.models import Donation as Products_Donations


from save_donation_fun import save_case_donation, extract_numbers
from django.urls import reverse
# import requests
# from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import Order
# Create your views here.
import time
# from urllib.parse import urlencode
# from django.conf import settings
from .kashier_payment import KashierPayment
import uuid

def checkout(request):
    return render(request, 'checkout/checkout.html')

def payment_success(request):
    return render(request, 'checkout/payment_success.html')

def payment_failed(request):
    return render(request, 'checkout/payment_failed.html')



@csrf_exempt
def start_payment(request):
    if request.method == "POST":

        donor_name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        cart_data = request.POST.get("cart_data")

        errors = []

        if not donor_name:
            errors.append("الاسم مطلوب")
        if not email:
            errors.append("البريد الإلكتروني مطلوب")
        if not phone:
            errors.append("رقم الهاتف مطلوب")

        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("المبلغ غير صالح")
        except:
            errors.append("المبلغ غير صالح")

        try:
            cart = json.loads(cart_data) if cart_data else []
        except:
            errors.append("بيانات السلة غير صالحة")

        if errors:
            return render(request, "checkout/start_payment.html", {
                "errors": errors
            })

        
        ########################################################
        merchant_order_id = f"Order_{uuid.uuid4()}"
        
        # إنشاء كائن KashierPayment
        kashier = KashierPayment()
        
        # إعداد callback URL 
        callback_url = request.build_absolute_uri('/payment/callback/')
        
        # إنشاء رابط الدفع
        payment_url = kashier.create_payment_url(
            amount=amount,
            merchant_order_id=merchant_order_id,
            currency='EGP',
            callback_url=callback_url,
            allowed_methods='',  # اتركه فارغاً لجميع طرق الدفع، أو 'card,wallet'
            display='ar'  # 'ar' للعربية أو 'en' للإنجليزية
        )
        
        # حفظ بيانات الطلب في قاعدة البيانات (اختياري)
        # donation = Donation.objects.create(
        #     donor_name=name,
        #     phone=phone,
        #     amount=amount,
        #     # case_id=case_id,
        #     merchant_order_id=merchant_order_id,
        #     payment_status='pending'
        # )
        donation = Order.objects.create(
            donor_name=donor_name,
            merchant_order_id=merchant_order_id,
            email=email,
            phone=phone,
            amount=amount,
            payment_status = 'PENDING',
            cart_data=cart
        )
        
        # إعادة التوجيه لصفحة الدفع
        return redirect(payment_url)
    


    return render(request, 'checkout/start_payment.html')



def kashier_callback(request):
    """
    View للتعامل مع callback من kashier.io بعد إتمام الدفع
    """
    # جلب جميع معاملات query
    query_params = request.GET.dict()
    
    # التحقق من صحة signature
    kashier = KashierPayment()
    is_valid = kashier.validate_callback_signature(query_params)
    
    if not is_valid:
        # signature غير صحيح - قد يكون محاولة تلاعب
        return redirect('payment_failed')
    
    # جلب حالة الدفع
    payment_status = query_params.get('paymentStatus', '')
    merchant_order_id = query_params.get('merchantOrderId', '')
    # order_id = query_params.get('orderId', '')
    # amount = query_params.get('amount', '')
    # transaction_id = query_params.get('transactionId', '')
    
    if payment_status == 'SUCCESS':
        # الدفع تم بنجاح
        # تحديث حالة التبرع في قاعدة البيانات
        donation = Order.objects.filter(
            merchant_order_id=merchant_order_id).first()
        if donation:
            donation.payment_status = 'PAID'
            donation.save()
        #####################################################
        process_order(donation)

        return render(request, 'checkout/payment_success.html', context={'pay_success':True})
        # return redirect('payment_success')  # استبدل باسم URL الخاص بك
    
    else:
        donation = Order.objects.filter(
            merchant_order_id=merchant_order_id).first()
        if donation:
            donation.payment_status = 'FAILED'
            donation.save()
        #####################################################
        # الدفع فشل أو تم إلغاؤه
        return redirect('payment_failed')  # استبدل باسم URL الخاص بك










# 


def process_order(order):
    cart = order.cart_data
    donor_name = order.donor_name if order.donor_name else ""

    for item in cart:
        if item.get("dataType") == "cases":
            save_case_donation(
                donor_name=donor_name,
                id=item["id"],
                name=item["name"],
                amount=item["quantity"],
                is_paid=True,
                payment_method="kashier"
            )

        elif item.get("dataType") == "products":
            try:
                product = Product.objects.get(id=extract_numbers(item["id"]))
                Products_Donations.objects.create(
                    donor_name=donor_name,
                    product=product,
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"],
                    payment_method="kashier",
                    product_image=item.get("img"),
                    is_paid = True,
                )
            except Product.DoesNotExist:
                Products_Donations.objects.create(
                    donor_name=donor_name,
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"],
                    payment_method="kashier",
                    product_image=item.get("img"),
                    is_paid = True,
                )
    ##################
    print('[+] Process Orders Done ')


