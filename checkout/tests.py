from django.test import TestCase

# Create your tests here.
from django.test import TestCase
import requests
from datetime import datetime, timedelta
# Create your tests here.
# url = 'https://api.kashier.io/v3/payment/sessions'
# SECRET_KEY = "6c4c9b33147cef528a59d52c2d749dae$8534350d9087e8bd53afdf6250b5927f6b1bb8444eee60e43d98b226ca8233acc90cfe4e791d787ce87696fc2344a7b7"
# API_KEY = '432e4f5f-511a-4bc9-85c9-7f85570c037b'

#test
# url = 'https://test-api.kashier.io/v3/payment/sessions'
# SECRET_KEY = "d2825285910dac7ab9f797071b4f6439$84167217b82ca3869f3d5070a05104226186ab1237a0aa5048ddc22ab8783f15b7989a7286fb71c833d38dc0e3ddac1b"
# API_KEY = 'd76a6ac4-90bb-4937-b7fd-4f38f912226a'



# expire_at = (datetime.utcnow() + timedelta(minutes=30)).isoformat() + "Z"
# MERCHANT_ID = "MID-1234-5678"  # Test Merchant ID
# ########################################################

# headers = {
#     "Authorization": SECRET_KEY,
#     "api-key": API_KEY,
#     "Content-Type": "application/json"
# }
# payload = {
#     "expireAt": expire_at,
#     "maxFailureAttempts": 3,
#     "paymentType": "paid",
#     "amount": f"{100.00:.2f}",
#     "currency": 'EGP',
#     "order": f"test_order_{int(datetime.utcnow().timestamp())}",
#     "merchantRedirect": "https://example.com/redirect",
#     "display": "en",
#     "type": "one-time",
#     "allowedMethods": "card,wallet",
#     "merchantId": MERCHANT_ID,
#     "description": "Test payment",
#     "customer": {
#         "email": 'test@gmail.com',
#         "reference": "12345"
#     },
#     "enable3DS": True,
#     "serverWebhook": "https://example.com/webhook"
#     }

# # response = requests.post(URL_LIVE, headers=headers, json=payload)

# # if response.status_code == 200:
# #     print(f"status: {response.json().get('status')}")
# #     print("Session created successfully:", response.json())
# # else:
# #     print("Error:", response.status_code, response.text)




def create_payment_session(amount,customer_email, redirect_url, display='ar'):
    # URL_LIVE = 'https://api.kashier.io/v3/payment/sessions'
    # URL_TEST = 'https://test-api.kashier.io/v3/payment/sessions'


    url = 'https://test-api.kashier.io/v3/payment/sessions'



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


# تجربة التشغيل
if __name__ == "__main__":
    create_payment_session(
        amount="1",
        customer_email="mogamalcode@gmail.com",
        redirect_url='https://lisette-notional-wen.ngrok-free.dev/en/kashier_webhook/',
        # display='en'
    )
