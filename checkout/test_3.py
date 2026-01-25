import hmac
import hashlib
import time
from urllib.parse import urlencode


class KashierPayment:
    """
    Kashier.io Payment Helper (Plain Python)
    """

    def __init__(self, merchant_id, api_key, mode="test"):
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.mode = mode  # test أو live
        self.base_url = "https://checkout.kashier.io"

    def generate_order_hash(self, order_id, amount, currency="EGP"):
        """
        Generate required HMAC hash
        """
        path = f"/?payment={self.merchant_id}.{order_id}.{amount}.{currency}"

        return hmac.new(
            self.api_key.encode(),
            path.encode(),
            hashlib.sha256
        ).hexdigest()

    def create_payment_url(
        self,
        amount,
        order_id=None,
        currency="EGP",
        callback_url=None,
        allowed_methods="",
        display="ar"
    ):
        """
        Create Kashier checkout URL
        """
        if not order_id:
            order_id = str(int(time.time()))

        order_hash = self.generate_order_hash(order_id, amount, currency)

        params = {
            "merchantId": self.merchant_id,
            "orderId": order_id,
            "amount": amount,
            "currency": currency,
            "hash": order_hash,
            "mode": self.mode,
            "display": display,
        }

        if callback_url:
            params["merchantRedirect"] = callback_url

        if allowed_methods:
            params["allowedMethods"] = allowed_methods

        return f"{self.base_url}?{urlencode(params)}"

    def validate_callback_signature(self, query_params: dict):
        """
        Validate callback signature
        """
        query_string = (
            f"paymentStatus={query_params.get('paymentStatus','')}"
            f"&cardDataToken={query_params.get('cardDataToken','')}"
            f"&maskedCard={query_params.get('maskedCard','')}"
            f"&merchantOrderId={query_params.get('merchantOrderId','')}"
            f"&orderId={query_params.get('orderId','')}"
            f"&cardBrand={query_params.get('cardBrand','')}"
            f"&orderReference={query_params.get('orderReference','')}"
            f"&transactionId={query_params.get('transactionId','')}"
            f"&amount={query_params.get('amount','')}"
            f"&currency={query_params.get('currency','')}"
        )

        generated_signature = hmac.new(
            self.api_key.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()

        return generated_signature == query_params.get("signature")









# from kashier_payment import KashierPayment

kashier = KashierPayment(
    merchant_id="MID-23552-762",
    api_key="d76a6ac4-90bb-4937-b7fd-4f38f912226a",
    mode="test"
)

payment_url = kashier.create_payment_url(
    amount=1,
    order_id="donationsfsgd4_111111",
    callback_url="http://127.0.0.1:8000/",
    display="ar"
)

print(payment_url)
