import hashlib
import json
import urllib.parse
import requests
from datetime import datetime, timedelta

# ====== بيانات التاجر ======
MERCHANT_ID = "MID-23552-762"
SECRET_KEY = "d2825285910dac7ab9f797071b4f6439$84167217b82ca3869f3d5070a05104226186ab1237a0aa5048ddc22ab8783f15b7989a7286fb71c833d38dc0e3ddac1b"  # السر اللي واخده من Kashier
MODE = "test"  # أو test live
API_KEY = 'd76a6ac4-90bb-4937-b7fd-4f38f912226a'


# بيانات الطلب
order_id = "ORDER_6464642655454643"
amount = "44"
currency = "EGP"

# البيانات الإضافية اللي هتبان للعميل
metadata = {
    "name": "Nor",
    "phone": "01066847767",
    "donateField": "تبرع عام"
}

# تحويل metadata إلى URL encoded
meta_encoded = urllib.parse.quote(json.dumps(metadata, ensure_ascii=False))

# إنشاء hash للدفع
hash_string = f"{MERCHANT_ID}{order_id}{amount}{currency}{SECRET_KEY}"
hash_value = hashlib.sha256(hash_string.encode()).hexdigest()

# تكوين رابط الدفع النهائي
checkout_url = (
    "https://checkout.kashier.io/?"
    f"merchantId={MERCHANT_ID}"
    f"&orderId={order_id}"
    f"&amount={amount}"
    f"&currency={currency}"
    f"&hash={hash_value}"
    f"&mode={MODE}"
    f"&metaData={meta_encoded}"
    "&allowedMethods=card"
    "&display=ar"
    "&merchantRedirect=https://www.diyarna.org"
    "&endDate=10-12-2027"
)

# print(checkout_url)

import requests

url = "https://api.diyarna.org/donation/saveLiveDonation"
data = {
    "name": "Nor",
    "phone": "01066847767",
    "address": "مصر",
    "amount": "44",
    "donateField": "تبرع عام"
}
response = requests.post(url, json=data)
# بيانات الطلب
print(response.json())


order_id = "ORDER_6464642655454643"
amount = "44"
currency = "EGP"
expire_at = (datetime.utcnow() + timedelta(days=3)).isoformat() + "Z"  

metadata = {
    "name": "Nor",
    "phone": "01066847767",
    "donateField": "تبرع عام"
}

meta_encoded = json.dumps(metadata, ensure_ascii=False)

data = {
    "expireAt": expire_at,
    "maxFailureAttempts": 3,
    "paymentType": "credit",
    "amount": amount,
    "currency": currency,
    "order": order_id,
    "merchantId": MERCHANT_ID,
    "metaData": metadata,
    "description": "تبرع عام",
    "allowedMethods": "card,wallet",
    "merchantRedirect": "https://www.diyarna.org/donation/donate",
    "display": "ar",
    "failureRedirect": False,
    "customer": {   
        "reference": order_id,  
        "email": "nor@example.com"
    }
}
headers = {
    "Authorization": SECRET_KEY,
    "api-key": API_KEY,
    "Content-Type": "application/json"
}
# response = requests.post(
#     "https://test-api.kashier.io/v3/payment/sessions",
#     headers=headers,
#     data=json.dumps(data)
# )

# print(response.status_code)
# print(response.json())