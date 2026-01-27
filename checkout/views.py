from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from donations.models import Case, Donation
from products.models import ProductOrder, Product
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


def checkout(request):
    return render(request, 'checkout/checkout.html')

def payment_success(request):
    return render(request, 'checkout/payment_success.html')

def payment_failed(request):
    return render(request, 'checkout/payment_failed.html')

# def create_payment_session(amount,customer_email, redirect_url, display='ar'):
#     # LIVE 
#     url = 'https://api.kashier.io/v3/payment/sessions'
#     SECRET_KEY = "6c4c9b33147cef528a59d52c2d749dae$8534350d9087e8bd53afdf6250b5927f6b1bb8444eee60e43d98b226ca8233acc90cfe4e791d787ce87696fc2344a7b7"
#     API_KEY = '432e4f5f-511a-4bc9-85c9-7f85570c037b'

#     #test
#     # url = 'https://test-api.kashier.io/v3/payment/sessions'
#     # SECRET_KEY = "d2825285910dac7ab9f797071b4f6439$84167217b82ca3869f3d5070a05104226186ab1237a0aa5048ddc22ab8783f15b7989a7286fb71c833d38dc0e3ddac1b"
#     # API_KEY = 'd76a6ac4-90bb-4937-b7fd-4f38f912226a'
#     #####################################################################
#     merchantId = "MID-23552-762"
#     order = f"ORDER-{int(datetime.utcnow().timestamp())}"
#     payload = {
#         "merchantId": merchantId,   # Merchant ID الحقيقي
#         "amount": str(amount),                   
#         "currency": "EGP",
#         "order": order,
#         "paymentType": "credit",
#         "allowedMethods": "card,wallet",
#         "type": "one-time",
#         "display": display,
#         "merchantRedirect": redirect_url,
#         "interactionSource": "ECOMMERCE",
#         "enable3DS": True,
#         "customer": {
#             "email": customer_email,
#             "reference": order # 
#         }
#     }

#     headers = {
#         "Authorization": SECRET_KEY,
#         "api-key": API_KEY,
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code in (200, 201):
#         data = response.json()
#         print("✅ Session Created Successfully")
#         print("Session ID:", data["_id"])
#         print("Session URL:", data["sessionUrl"])
#         return data["sessionUrl"]
#     else:
#         print("❌ Failed to create session")
#         print("Status:", response.status_code)
#         print(response.text)
#         return None


@csrf_exempt
def start_payment(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        cart_data = request.POST.get("cart_data")

        errors = []

        if not name:
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
        merchant_order_id = f"Order_{int(time.time())}"
        
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

    for item in cart:
        if item.get("dataType") == "cases":
            save_case_donation(
                id=item["id"],
                name=item["name"],
                amount=item["quantity"],
                is_paid=True,
                payment_method="kashier"
            )

        elif item.get("dataType") == "products":
            try:
                product = Product.objects.get(id=extract_numbers(item["id"]))
                ProductOrder.objects.create(
                    product=product,
                    buyer_name=item["name"],
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"],
                    payment_method="kashier",
                    product_image=item.get("img")
                )
            except Product.DoesNotExist:
                ProductOrder.objects.create(
                    buyer_name=item["name"],
                    quantity=item["quantity"],
                    total_price=item["price"] * item["quantity"],
                    payment_method="kashier",
                    product_image=item.get("img"),
                    is_paid = True,
                )
    ##################
    print(f'process_order Done')


