# ملف الفورم
from django import forms
class PostForm(forms.ModelForm):
    class Meta:
        model = Order # اسم الموديل بتاعك
        fields = ['order_reference', 'email'] # الحقول اللي انا عاوزها
        # exclude = ['created_at', 'user']  # كل الحقول هتكون موجودة ما عدا الحقول دي




# الداله 
def test_form(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # جلب البيانات بعد التحقق
            email = form.cleaned_data['email']
            print(email)
            # منع إعادة POST عند الريلود
            return redirect('test_form')
    else:
        form = PostForm()

    return render(request, 'test/test_form.html', {'form': form})