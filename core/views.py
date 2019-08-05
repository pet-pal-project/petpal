from django.shortcuts import render, redirect
from core.models import Pet, Visit, Checklist, Task, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from core.forms import ProfileUpdateForm, ProfileForm, ChecklistForm, AddAPetForm
from django.shortcuts import get_object_or_404



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

def add_checklist(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            sitter = form.cleaned_data.get('sitter')
            date = form.cleaned_data.get('date')
            task1 = form.cleaned_data.get('task1')
            task2 = form.cleaned_data.get('task2')
            task3 = form.cleaned_data.get('task3')
            task4 = form.cleaned_data.get('task4')
            task5 = form.cleaned_data.get('task5')
            new_visit = Visit(sitter_id=sitter, due_date_on=date)    
            new_visit.save()

            return redirect('home')
    else:
        form = ChecklistForm()
    return render(request, 'add_checklist.html', {'form': form})




def sitter_arrived(request):
    send_mail(
        'Your sitter has arrived.',
        'Hi { owner }, we are notifiying you that your sitter, { sitter } , has successfully checked in for their visit today.',
        'admin@pet-pal.com',
        ['amanda.minton@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def sitter_departed(request):
    send_mail(
        'Visit for today is complete.',
        'Hi { owner }, we are notifiying you that your sitter, { sitter } , has successfully checked out from their visit today. To reveiew their completed tasks, click here',
        'admin@pet-pal.com',
        ['amanda.minton@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def critical_task_missed(request):
    send_mail(
        'Critical task for today NOT marked complete.',
        'Hi { owner }, we are notifiying you that our system does not yet have a record of {the critical task} being marked complete for the visit today. To reveiew tasks, please click here',
        'admin@pet-pal.com',
        ['amanda.minton@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def critical_task_complete(request):
    send_mail(
        'Your sitter has completed a critical task for today.',
        'Hi { owner }, we are notifiying you that our system shows {sitter} has marked {the critical task} complete for the visit today. To reveiew tasks, please click here',
        'admin@pet-pal.com',
        ['amanda.minton@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')

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



def add_a_pet(request):
    if request.method == 'POST':
        form = AddAPetForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            animal = form.cleaned_data.get('animal')
            breed = form.cleaned_data.get('breed')
            color_and_Markings= form.cleaned_data.get('color_and_Markings')
            weight_in_lbs = form.cleaned_data.get('weight_in_lbs')
            age = form.cleaned_data.get('age')
            sex = form.cleaned_data.get('sex') 
            # profile_Image = form.cleaned_data.get('profile_Image')
            owner = form.cleaned_data.get('owner')
            about_Me = form.cleaned_data.get('about_Me')
            vet_Info = form.cleaned_data.get('vet_Info')
            emergency_Contact = form.cleaned_data.get('emergency_Contact')
        return redirect("home")
    else:
        form = AddAPetForm()
    return render(request, 'add_pet.html', {'form': form})


def add_pet(request):
    if request.method == 'POST':
        form = AddAPetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AddAPetForm()
    return render(request, 'add_pet.html', {'form': form})  