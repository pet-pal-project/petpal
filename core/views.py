from django.shortcuts import render, redirect
from core.models import Pet, Visit, Checklist, Task, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.mail import send_mail
from core.forms import ProfileUpdateForm, ProfileForm, ChecklistForm, AddAPetForm, UserForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime




# Create your views here.


        

@login_required
def index(request):
    my_pet_list = Pet.objects.filter(owner=request.user)
    my_visits = Visit.objects.filter(sitter_id=request.user)
    all_checklists = Checklist.objects.all()
    all_tasks = Task.objects.all()


    context = {
        'my_pet_list': my_pet_list,
        'my_visits': my_visits,
        'all_checklists': all_checklists,
        'all_tasks': all_tasks,
    }
    return render(request, 'dashboard.html', context=context)

def pet_detail(request,pk):
    my_pet_list = Pet.objects.filter(owner=request.user)
    pet = Pet.objects.get(pk=pk)
    pet_checklists = Checklist.objects.filter(pet_id=pet)
    all_tasks = Task.objects.all()
    all_checklists = Checklist.objects.all()

    pet_tasks = []

    for task in all_tasks:
        if task.checklist_id.pet_id == pet and task.checklist_id.visit.due_date_on == task.checklist_id.visit.due_date_on:
            pet_tasks.append(task)
    
    # print(pet_tasks)

    if request.method == 'POST':
        tasks_checked = request.POST.getlist('task')
        for task_checked in tasks_checked:
            task_id = int(task_checked)
            task_completed = Task.objects.get(id=task_id)
            task_completed.completed_on=datetime.datetime.now()
            task_completed.save()
        return HttpResponseRedirect(request.path_info)

    return render(request, 'pet-detail.html', {
        'pet' : pet,
        'all_tasks': all_tasks,
        'all_checklists': all_checklists,
        'pet_checklists': pet_checklists,
        'my_pet_list': my_pet_list,
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
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            sitter = form.cleaned_data.get('sitter') 
            task1 = form.cleaned_data.get('task1')
            task2 = form.cleaned_data.get('task2')
            task3 = form.cleaned_data.get('task3')
            task4 = form.cleaned_data.get('task4')
            task5 = form.cleaned_data.get('task5')
            print (start_date)
            print (end_date)
            delta = end_date - start_date
            print(delta.days)
            existing_visit = Visit.objects.filter(sitter_id=sitter).filter(due_date_on=start_date)
            num_of_days = delta.days
            if delta.days == 0:
                if existing_visit:
                    visitpk = existing_visit[0]
                    new_checklist = Checklist.objects.filter(visit=visitpk).filter(pet_id=pet)
                    new_task1 = Task(description=task1, checklist_id=new_checklist[0])
                    new_task1.save()
                    new_task2 = Task(description=task2, checklist_id=new_checklist[0])
                    new_task2.save()
                    new_task3 = Task(description=task3, checklist_id=new_checklist[0])
                    new_task3.save()
                    new_task4 = Task(description=task4, checklist_id=new_checklist[0])
                    new_task4.save()
                    new_task5 = Task(description=task5, checklist_id=new_checklist[0])
                    new_task5.save()
                    print("EXISTING VISIT WITH DATE AND USER")
                else:
                    new_visit = Visit(sitter_id=sitter, due_date_on=start_date)    
                    new_visit.save()
                    visit_id = new_visit.pk
                    new_checklist = Checklist(visit=new_visit, pet_id=pet)
                    new_checklist.save()
                    new_task1 = Task(description=task1, checklist_id=new_checklist)
                    new_task1.save()
                    new_task2 = Task(description=task2, checklist_id=new_checklist)
                    new_task2.save()
                    new_task3 = Task(description=task3, checklist_id=new_checklist)
                    new_task3.save()
                    new_task4 = Task(description=task4, checklist_id=new_checklist)
                    new_task4.save()
                    new_task5 = Task(description=task5, checklist_id=new_checklist)
                    new_task5.save()
                    print("A NEW VISIT WITH DATE AND USER")
            else:
                for day in range(num_of_days+1):
                    print("MORE THAN ONE DAY!")
                    current_date = start_date + datetime.timedelta(days=day)
                    existing_visit = Visit.objects.filter(sitter_id=sitter).filter(due_date_on=current_date)
                
                    if existing_visit:
                        visitpk = existing_visit[0]
                        new_checklist = Checklist.objects.filter(visit=visitpk).filter(pet_id=pet)
                        new_task1 = Task(description=task1, checklist_id=new_checklist[0])
                        new_task1.save()
                        new_task2 = Task(description=task2, checklist_id=new_checklist[0])
                        new_task2.save()
                        new_task3 = Task(description=task3, checklist_id=new_checklist[0])
                        new_task3.save()
                        new_task4 = Task(description=task4, checklist_id=new_checklist[0])
                        new_task4.save()
                        new_task5 = Task(description=task5, checklist_id=new_checklist[0])
                        new_task5.save()
                        print("SAME DAY")
                    else:
                        new_visit = Visit(sitter_id=sitter, due_date_on=current_date)    
                        new_visit.save()
                        visit_id = new_visit.pk
                        new_checklist = Checklist(visit=new_visit, pet_id=pet)
                        new_checklist.save()
                        new_task1 = Task(description=task1, checklist_id=new_checklist)
                        new_task1.save()
                        new_task2 = Task(description=task2, checklist_id=new_checklist)
                        new_task2.save()
                        new_task3 = Task(description=task3, checklist_id=new_checklist)
                        new_task3.save()
                        new_task4 = Task(description=task4, checklist_id=new_checklist)
                        new_task4.save()
                        new_task5 = Task(description=task5, checklist_id=new_checklist)
                        new_task5.save()
                        print("DIFFERENT DAYS")



            
            return redirect('home')
    else:
        form = ChecklistForm()
        
    return render(request, 'add_checklist.html', {'form': form, 'pet' : pet,})



def new_pet_notification(request, user):
    send_mail(
        'You have created a new animal profile.',
        f'Hi { user.username }, we are notifiying you that your a new animal profile has been successfully created!',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )

    return render(request, 'email.html')
    
    return HttpResponse('Mail successfully sent')



def sitter_arrived(request):
    send_mail(
        'Your sitter has arrived.',
         f'Hi { user.username }, we are notifiying you that your sitter, { sitter } , has successfully checked in for their visit today.',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def sitter_departed(request):
    send_mail(
        'Visit for today is complete.',
         f'Hi { user.username }, we are notifiying you that your sitter, { sitter } , has successfully checked out from their visit today. To reveiew their completed tasks, click here',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def critical_task_missed(request):
    send_mail(
        'Critical task for today NOT marked complete.',
         f'Hi { user.username }, we are notifiying you that our system does not yet have a record of a critical task being marked complete for the visit today. To reveiew tasks, please click here',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')


def critical_task_complete(request):
    send_mail(
        'Your sitter has completed a critical task for today.',
         f'Hi { user.username }, we are notifiying you that our system shows sitter has marked  a critical task complete for the visit today. To reveiew tasks, please click here',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )

    return HttpResponse('Mail successfully sent')

@login_required
def update_profile(request):
        user = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=request.user)
        if request.method == "POST":
            form = ProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
            return redirect(to='home')
        else:
            form = ProfileForm(instance=request.user)
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
            user = request.user
            new_pet_notification(request, user)
            print("email sent")

            new_pet = form.save(commit=False)
            new_pet.owner = request.user
            new_pet.save()

            return redirect("home")
    else:
        form = AddAPetForm()
    return render(request, 'add_pet.html', {'form': form})  


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(to='home')
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'update_profile.html', context)

