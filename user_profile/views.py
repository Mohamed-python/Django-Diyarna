from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
# Create your views here.

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile_view.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile = request.user.profile  # نجيب بروفايل اليوزر
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile')  
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile_edit.html', {'form': form})