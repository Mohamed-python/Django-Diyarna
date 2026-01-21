from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from .form import VolunteerForm

def volunteer_create(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            if volunteer.volunteer_type == 'individual':
                volunteer.group_size = None
            volunteer.save()
            return redirect('volunteers:volunteer_success')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer.html', {'form': form})



def volunteer_success(request):
    return render(request, 'volunteer_success.html')
