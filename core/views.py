from django.shortcuts import render, redirect
from core.models import Pet, Routine, Critical, Profile, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from core.forms import ProfileUpdateForm, ProfileForm


# Create your views here.

@login_required
def index(request):
    my_pet_list = Pet.objects.filter(owner=request.user)

    context = {
        'my_pet_list': my_pet_list,
    }
    return render(request, 'dashboard.html', context=context)

def pet_detail(request,pk):
    pet = Pet.objects.get(pk=pk)
 
    return render(request, 'pet-detail.html', {
        'pet' : pet,
      
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required
def update_profile(request):
    
        current_user = request.user
        user = Profile.objects.get(user=current_user)
  
        if request.method == "POST":
            form = ProfileForm(request.POST,instance=user)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
            return redirect(to='home')
        else:
            form = ProfileForm()
        return render(request, 'update_profile.html', {'form': form})