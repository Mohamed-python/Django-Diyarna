from django.shortcuts import render, get_object_or_404, redirect
from .models import Case, Donation
from .forms import DonationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

######################################
from save_donation_fun import save_case_donation, extract_numbers
from django.urls import reverse
from django.http import JsonResponse

from donations.models import Case, Donation
from products.models import ProductOrder, Product

######################################




# Create your views here.
def donations_list(request):

    cases = Case.objects.order_by('-created_at')[:6]  # جلب كل الحالات

    return render(request, 'donations/donations_all.html', {'cases': cases})

# def hi(request):
#     cases = Case.objects.all()  # جلب كل الحالات
#     return render(request, 'donations/hi.html', {'cases': cases})


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


    return redirect('checkout')


def donate(request, slug):
    case = get_object_or_404(Case, slug=slug)

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


