import hmac
import hashlib
from urllib.parse import urlencode
from django.conf import settings
import time


######################
class KashierPayment:
    """
    كلاس لإنشاء وإدارة طلبات الدفع مع kashier.io
    """
    
    def __init__(self):
        # استبدل هذه القيم بـ API keys الخاصة بك من kashier.io
        self.mid = getattr(settings, 'KASHIER_MID', 'your_merchant_id_here')  # Merchant ID مثل: MID-xx-xx
        self.api_key = getattr(settings, 'KASHIER_API_KEY', 'your_api_key_here')  # API Key من لوحة التحكم
        self.mode = getattr(settings, 'KASHIER_MODE', 'test')  # 'test' أو 'live'
        self.base_url = 'https://checkout.kashier.io' if self.mode == 'live' else 'https://checkout.kashier.io'
    
    def generate_order_hash(self, merchant_order_id, amount, currency='EGP'):
        """
        إنشاء hash للطلب (مطلوب من kashier.io)
        
        Parameters:
        -----------
        merchant_order_id : str
            معرف الطلب الفريد الخاص بك
        amount : float
            المبلغ المراد دفعه
        currency : str
            العملة (افتراضي: EGP)
        
        Returns:
        --------
        str : hash المطلوب للطلب
        """
        # بناء path للـ hash
        path = f"/?payment={self.mid}.{merchant_order_id}.{amount}.{currency}"
        
        # إنشاء hash باستخدام HMAC SHA256
        hash_value = hmac.new(
            self.api_key.encode('utf-8'),
            path.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hash_value
    
    def create_payment_url(self, amount, merchant_order_id=None, currency='EGP', 
                          callback_url=None, allowed_methods='', display='ar'):
        """
        إنشاء رابط الدفع من kashier.io
        
        Parameters:
        -----------
        amount : float
            المبلغ المراد دفعه
        merchant_order_id : str
            معرف الطلب الفريد (إذا لم يتم توفيره، سيتم إنشاء واحد تلقائياً)
        currency : str
            العملة (افتراضي: EGP)
        callback_url : str
            رابط callback بعد إتمام الدفع
        allowed_methods : str
            طرق الدفع المسموحة (مثل: 'card,wallet' أو اتركه فارغاً لجميع الطرق)
        display : str
            لغة العرض ('ar' أو 'en')
        
        Returns:
        --------
        str : رابط الدفع الكامل
        """
        # إنشاء معرف طلب فريد إذا لم يتم توفيره
        if not merchant_order_id:
            merchant_order_id = str(int(time.time()))
        
        # إنشاء hash للطلب
        order_hash = self.generate_order_hash(merchant_order_id, amount, currency)
        
        # بناء معاملات URL
        params = {
            'merchantId': self.mid,
            'orderId': merchant_order_id,
            'mode': self.mode,
            'amount': str(amount),
            'currency': currency,
            'hash': order_hash,
            'display': display
        }
        
        # إضافة callback URL إذا تم توفيره
        if callback_url:
            params['merchantRedirect'] = callback_url
        
        # إضافة طرق الدفع المسموحة إذا تم توفيرها
        if allowed_methods:
            params['allowedMethods'] = allowed_methods
        
        # بناء URL الكامل
        payment_url = f"{self.base_url}?{urlencode(params)}"
        
        return payment_url
    
    def validate_callback_signature(self, query_params):
        """
        التحقق من صحة signature في callback من kashier.io
        
        Parameters:
        -----------
        query_params : dict
            معاملات query من callback URL
        
        Returns:
        --------
        bool : True إذا كان signature صحيح
        """
        # بناء query string للتحقق (بدون signature)
        query_string = (
            f"&paymentStatus={query_params.get('paymentStatus', '')}"
            f"&cardDataToken={query_params.get('cardDataToken', '')}"
            f"&maskedCard={query_params.get('maskedCard', '')}"
            f"&merchantOrderId={query_params.get('merchantOrderId', '')}"
            f"&orderId={query_params.get('orderId', '')}"
            f"&cardBrand={query_params.get('cardBrand', '')}"
            f"&orderReference={query_params.get('orderReference', '')}"
            f"&transactionId={query_params.get('transactionId', '')}"
            f"&amount={query_params.get('amount', '')}"
            f"&currency={query_params.get('currency', '')}"
        )
        
        # إزالة & الأول
        final_url = query_string[1:] if query_string.startswith('&') else query_string
        
        # إنشاء hash للتحقق
        signature = hmac.new(
            self.api_key.encode('utf-8'),
            final_url.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # مقارنة مع signature المرسل
        received_signature = query_params.get('signature', '')
        
        return signature == received_signature

