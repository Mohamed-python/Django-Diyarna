from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from donations.models import Case, Donation
from products.models import ProductOrder, Product
from save_donation_fun import save_case_donation, extract_numbers
from django.urls import reverse
import requests
from datetime import datetime, timedelta
import requests
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import Order
# Create your views here.
# def payment(request):
#     return render(request, 'Data_Payment.html')

def create_payment_session(amount,customer_email, redirect_url, display='ar'):
    # LIVE 
    # url = 'https://api.kashier.io/v3/payment/sessions'
    # SECRET_KEY = "d2825285910dac7ab9f797071b4f6439$84167217b82ca3869f3d5070a05104226186ab1237a0aa5048ddc22ab8783f15b7989a7286fb71c833d38dc0e3ddac1b"
    # API_KEY = 'd76a6ac4-90bb-4937-b7fd-4f38f912226a'

    #test
    url = 'https://test-api.kashier.io/v3/payment/sessions'
    SECRET_KEY = "d2825285910dac7ab9f797071b4f6439$84167217b82ca3869f3d5070a05104226186ab1237a0aa5048ddc22ab8783f15b7989a7286fb71c833d38dc0e3ddac1b"
    API_KEY = 'd76a6ac4-90bb-4937-b7fd-4f38f912226a'
    #####################################################################
    merchantId = "MID-23552-762"
    order = f"ORDER-{int(datetime.utcnow().timestamp())}"
    payload = {
        "merchantId": merchantId,   # Merchant ID الحقيقي
        "amount": str(amount),                   
        "currency": "EGP",
        "order": order,
        "paymentType": "credit",
        "allowedMethods": "card,wallet",
        "type": "one-time",
        "display": display,
        "merchantRedirect": redirect_url,
        "interactionSource": "ECOMMERCE",
        "enable3DS": True,
        "customer": {
            "email": customer_email,
            "reference": order # 
        }
    }

    headers = {
        "Authorization": SECRET_KEY,
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (200, 201):
        data = response.json()
        print("✅ Session Created Successfully")
        print("Session ID:", data["_id"])
        print("Session URL:", data["sessionUrl"])
        return data["sessionUrl"]
    else:
        print("❌ Failed to create session")
        print("Status:", response.status_code)
        print(response.text)
        return None


@csrf_exempt
# def start_payment(request):
#     if request.method == 'POST':
#         print(f'start_payment POST')
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         amount = request.POST.get("amount")
#         cart_data = request.POST.get("cart_data")

#         errors = []

#         if not name:
#             errors.append("الاسم مطلوب")
#         if not email:
#             errors.append("البريد الإلكتروني مطلوب")
#         if not phone:
#             errors.append("رقم الهاتف مطلوب")
#         if not amount:
#             errors.append("المبلغ غير صالح")


#         try:
#             cart = json.loads(cart_data) if cart_data else []
#         except json.JSONDecodeError:
#             errors.append("بيانات السلة غير صالحة")


        
#         # if errors:
#         #     return redirect('start_payment')

#         # رقم طلب فريد
#         order_reference = f"ORDER-{int(now().timestamp())}"

#         # هنا مؤقتًا بنعرض الداتا
#         # الخطوة اللي بعدها: إنشاء Kashier Session
#         context = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "amount": amount,
#             "cart": cart,
#             "order_reference": order_reference
#         }

#         ###################################
#         session_id = create_payment_session(
#             amount = amount,
#             customer_email = email,
#             redirect_url = 'https://lisette-notional-wen.ngrok-free.dev/checkout/',
#         )
#         print("##################################################################")
#         if session_id:
#             return render(request, "checkout/checkout.html", context={'session_id':session_id})
    
#     print('ddddddddddddddddddddddddddd')
#     return render(request, "checkout/start_payment.html")
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

        order_reference = f"ORDER-{int(now().timestamp())}"

        # 🔹 إنشاء Order PENDING
        Order.objects.create(
            order_reference=order_reference,
            email=email,
            phone=phone,
            amount=amount,
            cart_data=cart
        )

        session_url = create_payment_session(
            amount=amount,
            customer_email=email,
            # merchant_order_id=order_reference,
            redirect_url="https://lisette-notional-wen.ngrok-free.dev/kashier_webhook/"
        )

        if not session_url:
            return render(request, "checkout/start_payment.html", {
                "errors": ["فشل إنشاء جلسة الدفع"]
            })

        return render(request, "checkout/checkout.html", {
            "session_id": session_url
        })

    return render(request, "checkout/start_payment.html")

# @csrf_exempt
def checkout(request):
    # if request.method == 'POST':
    #     return render(request, 'checkout/checkout_success.html')

    return render(request, 'checkout/checkout.html')




def donations_success(request):
    return render(request, 'checkout/checkout_success.html')


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
                    product_image=item.get("img")
                )


@csrf_exempt
def kashier_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_ref = data.get("order_reference")  # ← مهم
        response = data.get("data", {})

        try:
            order = Order.objects.get(order_reference=order_ref)
        except Order.DoesNotExist:
            return JsonResponse({"error": "order not found"}, status=404)

        payment_status = response.get("status") or response.get("result")
        transaction_id = response.get("transactionId")

        if payment_status in ["SUCCESS", "CAPTURED"]:
            if order.status != "PAID":
                order.status = "PAID"
                order.transaction_id = transaction_id
                order.save()
                process_order(order)

            return JsonResponse({"status": "ok"})

        order.status = "FAILED"
        order.save()
        return JsonResponse({"status": "failed"})

    # GET redirect
    if request.method == "GET":
        payment_status = request.GET.get("paymentStatus")
        if payment_status == "SUCCESS":
            return render(request, "checkout/checkout_success.html")
        return render(request, "checkout/checkout_failed.html")

    return JsonResponse({"error": "Method not allowed"}, status=405)




@csrf_exempt
def order_completed(request):
    # success_donate = None
    if request.method == 'POST':
        print("Poooooooooooost order_completed")
        data = json.loads(request.body.decode('utf-8'))
        cart = data.get('cart', [])
        # print(cart)
        for item in cart:
            data_type = item.get('dataType')
            # print(data_type)

            # تحديد الموديل المناسب
            model = None
            if data_type == "cases":
                model = Case
                ###########
                donate = save_case_donation(id=item['id'], name=item['name'], amount=item['quantity'],is_paid=True, payment_method='vodafone')
                if donate:
                    print(f"Donate Case success id => {donate}")

            elif data_type == "products":
                model = Product
                # print(item)
                try:
                    product = Product.objects.get(id=extract_numbers(item.get('id')))
                    donate_product = ProductOrder.objects.create(
                        product=product,
                        buyer_name=item.get('name'),
                        quantity=item.get('quantity', 1),
                        total_price=item.get('price') * item.get('quantity', 1),
                        payment_method=item.get('payment_method', 'cash'),
                        product_image=item.get('img')  # نخزن رابط الصورة فقط
                    )
                    print(f"Donate ProductOrder success id => {donate_product.id}")

                except Product.DoesNotExist:
                    # لو المنتج اتحذف مسبقًا
                    donate_product = ProductOrder.objects.create(
                        buyer_name=item.get('name'),
                        quantity=item.get('quantity', 1),
                        total_price=item.get('price') * item.get('quantity', 1),
                        payment_method=item.get('payment_method', 'cash'),
                        product_image=item.get('image_path')  # لو عندك رابط الصورة في السلة
                    )
                    print(f"Create ProductOrder success id => {donate_product.id}")

            else:
                continue  # لو النوع غير معروف، تجاهله



            # جلب object الأصلي لو موجود
            # try:
            #     obj = model.objects.get(id=extract_numbers(item['id']))
            # except model.DoesNotExist:
            #     continue

            # # حفظ في CartItem
            # CartItem.objects.create(
            #     content_object=obj,
            #     name=item['name'],
            #     price=item['price'],
            #     quantity=item['quantity']
            # )

            ###############################
            
        redirect_url = reverse('donations_success')  # اسم الصفحة اللي هتتحول ليها
        return JsonResponse({
                'status': 'success',
                'redirect_url': redirect_url
            })
        
    

    return redirect('home')

