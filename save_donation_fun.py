from donations.models import Case, Donation
from products.models import ProductOrder, Product

#target_amount

def extract_numbers(s):
    return ''.join(c for c in s if c.isdigit())

def save_case_donation(id, name, amount, payment_method, is_paid):
    case = Case.objects.get(id=extract_numbers(id))
    donation = Donation.objects.create(
        case=case,
        name=name,
        amount=amount,
        payment_method=payment_method,
        is_paid=is_paid 
    )
    if donation and donation.id:
        return donation.id
    



# def save_product_order(id, name, quantity, price, payment_method, product_image):
#     product = Product.objects.get(id=id)
#     try:
#         product = Product.objects.get(id=id)
#         ProductOrder.objects.create(
#             product=product,
#             buyer_name=name,
#             quantity=quantity,
#             total_price=price * quantity,
#             payment_method=payment_method,
#             product_image=product_image  # نخزن رابط الصورة فقط
#         )
#         return product.id
#     except Product.DoesNotExist:
#         # لو المنتج اتحذف مسبقًا
#         ProductOrder.objects.create(
#             buyer_name=name,
#             quantity=quantity,
#             total_price=price * quantity,
#             payment_method=payment_method,
#             product_image=product_image  # لو عندك رابط الصورة في السلة
#         )

    
    


