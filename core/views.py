from django.shortcuts import render, redirect, get_object_or_404
from core.models import Pet, Visit, Checklist, Task, Profile, Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from core.forms import ProfileUpdateForm, ProfileForm, ChecklistForm, AddAPetForm, UserForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from twilio.rest import Client
import os
import environ

import datetime


# Create your views here.  
import datetime

      

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


@login_required
def pet_detail(request,pk):
    my_pet_list = Pet.objects.filter(owner=request.user)
    pet = Pet.objects.get(pk=pk)
    pet_checklists = Checklist.objects.filter(pet_id=pet)
    all_tasks = Task.objects.all()
    all_checklists = Checklist.objects.all()
    permitted = Contact.objects.filter(name=request.user).filter(user=pet.owner)


    pet_tasks = []

    for task in all_tasks:
        if task.checklist_id.pet_id == pet and task.checklist_id.visit.due_date_on == task.checklist_id.visit.due_date_on:
            pet_tasks.append(task)
    
    # print(pet_tasks)

    if request.method == 'POST':
        tasks_checked = request.POST.getlist('task')
        user = request.user
        tasks = tasks_checked
        sitter_departed_notification(request, user, tasks)
        for task_checked in tasks_checked:
            task_id = int(task_checked)
            task_completed = Task.objects.get(id=task_id)
            task_completed.completed_on=datetime.datetime.now()
            task_completed.save()
            account_sid = os.environ.get('account_sid')
            auth_token = os.environ.get('auth_token')
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                    body='Your sitter has checked out!',
                    from_='+19842144116',
                    to='+19192594909',
                )

            print(message.sid)
        

        return HttpResponseRedirect(request.path_info)

    return render(request, 'pet-detail.html', {
        'pet' : pet,
        'all_tasks': all_tasks,
        'all_checklists': all_checklists,
        'pet_checklists': pet_checklists,
        'my_pet_list': my_pet_list,
        'permitted': permitted,
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
def add_checklist(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        sitterform = UserForm(request.POST, user=request.user)
        if form.is_valid() and sitterform.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            sitter = sitterform.cleaned_data.get('sitter') 
            task1 = form.cleaned_data.get('task1')
            task2 = form.cleaned_data.get('task2')
            task3 = form.cleaned_data.get('task3')
            task4 = form.cleaned_data.get('task4')
            task5 = form.cleaned_data.get('task5')
            task6 = form.cleaned_data.get('task6')
            task7 = form.cleaned_data.get('task7')
            task8 = form.cleaned_data.get('task8')
            task9 = form.cleaned_data.get('task9')
            task10 = form.cleaned_data.get('task10')
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
                    if task1:
                        new_task1 = Task(description=task1, checklist_id=new_checklist[0])
                        new_task1.save()
                    if task2:
                        new_task2 = Task(description=task2, checklist_id=new_checklist[0])
                        new_task2.save()
                    if task3:
                        new_task3 = Task(description=task3, checklist_id=new_checklist[0])
                        new_task3.save()
                    if task4:
                        new_task4 = Task(description=task4, checklist_id=new_checklist[0])
                        new_task4.save()
                    if task5:
                        new_task5 = Task(description=task5, checklist_id=new_checklist[0])
                        new_task5.save()
                    if task6:
                        new_task6 = Task(description=task6, checklist_id=new_checklist[0])
                        new_task6.save()
                    if task7:
                        new_task7 = Task(description=task7, checklist_id=new_checklist[0])
                        new_task7.save()
                    if task8:
                        new_task8 = Task(description=task8, checklist_id=new_checklist[0])
                        new_task8.save()
                    if task9:
                        new_task9 = Task(description=task9, checklist_id=new_checklist[0])
                        new_task9.save()
                    if task10:
                        new_task10 = Task(description=task10, checklist_id=new_checklist[0])
                        new_task10.save()
                  

                    print("EXISTING VISIT WITH DATE AND USER")
                else:
                    new_visit = Visit(sitter_id=sitter, due_date_on=start_date)    
                    new_visit.save()
                    visit_id = new_visit.pk
                    new_checklist = Checklist(visit=new_visit, pet_id=pet)
                    new_checklist.save()

                    if task1:
                        new_task1 = Task(description=task1, checklist_id=new_checklist)
                        new_task1.save()
                    if task2:
                        new_task2 = Task(description=task2, checklist_id=new_checklist)
                        new_task2.save()
                    if task3:
                        new_task3 = Task(description=task3, checklist_id=new_checklist)
                        new_task3.save()
                    if task4:
                        new_task4 = Task(description=task4, checklist_id=new_checklist)
                        new_task4.save()
                    if task5:
                        new_task5 = Task(description=task5, checklist_id=new_checklist)
                        new_task5.save()
                    if task6:
                        new_task6 = Task(description=task6, checklist_id=new_checklist)
                        new_task6.save()
                    if task7:
                        new_task7 = Task(description=task7, checklist_id=new_checklist)
                        new_task7.save()
                    if task8:
                        new_task8 = Task(description=task8, checklist_id=new_checklist)
                        new_task8.save()
                    if task9:
                        new_task9 = Task(description=task9, checklist_id=new_checklist)
                        new_task9.save()
                    if task10:
                        new_task10 = Task(description=task10, checklist_id=new_checklist)
                        new_task10.save()
                    print("A NEW VISIT WITH DATE AND USER")
            else:
                for day in range(num_of_days+1):
                    print("MORE THAN ONE DAY!")
                    current_date = start_date + datetime.timedelta(days=day)
                    existing_visit = Visit.objects.filter(sitter_id=sitter).filter(due_date_on=current_date)
                
                    if existing_visit:
                        visitpk = existing_visit[0]
                        if task1:
                            new_task1 = Task(description=task1, checklist_id=new_checklist[0])
                            new_task1.save()
                        if task2:
                            new_task2 = Task(description=task2, checklist_id=new_checklist[0])
                            new_task2.save()
                        if task3:
                            new_task3 = Task(description=task3, checklist_id=new_checklist[0])
                            new_task3.save()
                        if task4:
                            new_task4 = Task(description=task4, checklist_id=new_checklist[0])
                            new_task4.save()
                        if task5:
                            new_task5 = Task(description=task5, checklist_id=new_checklist[0])
                            new_task5.save()
                        if task6:
                            new_task6 = Task(description=task6, checklist_id=new_checklist[0])
                            new_task6.save()
                        if task7:
                            new_task7 = Task(description=task7, checklist_id=new_checklist[0])
                            new_task7.save()
                        if task8:
                            new_task8 = Task(description=task8, checklist_id=new_checklist[0])
                            new_task8.save()
                        if task9:
                            new_task9 = Task(description=task9, checklist_id=new_checklist[0])
                            new_task9.save()
                        if task10:
                            new_task10 = Task(description=task10, checklist_id=new_checklist[0])
                            new_task10.save()
                            print("SAME DAY")
                    else:
                        new_visit = Visit(sitter_id=sitter, due_date_on=current_date)    
                        new_visit.save()
                        visit_id = new_visit.pk
                        new_checklist = Checklist(visit=new_visit, pet_id=pet)
                        new_checklist.save()
                        if task1:
                            new_task1 = Task(description=task1, checklist_id=new_checklist)
                            new_task1.save()
                        if task2:
                            new_task2 = Task(description=task2, checklist_id=new_checklist)
                            new_task2.save()
                        if task3:
                            new_task3 = Task(description=task3, checklist_id=new_checklist)
                            new_task3.save()
                        if task4:
                            new_task4 = Task(description=task4, checklist_id=new_checklist)
                            new_task4.save()
                        if task5:
                            new_task5 = Task(description=task5, checklist_id=new_checklist)
                            new_task5.save()
                        if task6:
                            new_task6 = Task(description=task6, checklist_id=new_checklist)
                            new_task6.save()
                        if task7:
                            new_task7 = Task(description=task7, checklist_id=new_checklist)
                            new_task7.save()
                        if task8:
                            new_task8 = Task(description=task8, checklist_id=new_checklist)
                            new_task8.save()
                        if task9:
                            new_task9 = Task(description=task9, checklist_id=new_checklist)
                            new_task9.save()
                        if task10:
                            new_task10 = Task(description=task10, checklist_id=new_checklist)
                            new_task10.save()
                        print("DIFFERENT DAYS")



            
            return redirect('home')
    else:
        form = ChecklistForm()
        sitterform = UserForm(user=request.user)

        
    return render(request, 'add_checklist.html', {'form': form, 'pet' : pet, 'sitterform': sitterform})



def new_pet_notification(request, user):
    send_mail(
        'You have created a new animal profile.',
        f'Hi { user.username }, we are notifiying you that you have successfully created a new animal profile!',
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )
    return render(request, 'email.html')
    return HttpResponse('Mail successfully sent')


# """ Notification to Sitter requesting visit acceptance."""
# def new_assignment_notification(request, user):
#     send_mail(
#         'New Assignment',
#         f'Hi { user.username }, we are notifiying you that { user.username } has requested to add you to an visist. Please log in to view and accept.',
#         'admin@critter-sitter.com',
#         [f'{ user.email }'],
#         fail_silently=False,
#     )
#     return render(request, 'email.html')
#     return HttpResponse('Mail successfully sent')


# """ Notification to Owner that the Sitter has arrived for their visit."""
# def sitter_arrived_notification(request, user):
#     send_mail(
#         'Your sitter has arrived.',
#          f'Hi { user.username }, we are notifiying you that your sitter, { sitter } , has successfully checked in for their visit today.',
#         'admin@critter-sitter.com',
#         [f'{ user.email }'],
#         fail_silently=False,
#     )
#     return render(request, 'email.html')
#     return HttpResponse('Mail successfully sent')



""" Notification to Owner that Sitter has checked out from their visit. Should include a list of completed tasks for that visit."""
def sitter_departed_notification(request, user, tasks):
    tasks = tasks
    send_mail(
        'Visit for today marked complete.',
         f'Hi { user.username }, we are notifiying you that your sitter, { user.username } , has successfully checked out from their visit today. Log in to account to view details: https://petz-app.herokuapp.com', 
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )
    return render(request, 'email.html')
    return HttpResponse('Mail successfully sent')


# """ For tasks marked as time-sensitive, that are not completed within the time allowed, a notification should be sent."""
# def critical_task_missed(request, user):
#     send_mail(
#         'Critical task for today NOT marked complete.',
#          f'Hi { user.username }, we are notifiying you that our system does not yet have a record of a critical task being marked complete for the visit today.',
#         'admin@critter-sitter.com',
#         [f'{ user.email }'],
#         fail_silently=False,
#     )
#     return render(request, 'email.html')
#     return HttpResponse('Mail successfully sent')


# """ Once a time-sensitive task is marked as complete, a notification should be sent."""
# def critical_task_complete(request, user):
#     send_mail(
#         'Your sitter has completed a critical task for today.',
#          f'Hi { user.username }, we are notifiying you that our system shows sitter has marked  a critical task complete for the visit today.',
#         'admin@critter-sitter.com',
#         [f'{ user.email }'],
#         fail_silently=False,
#     )
#     return render(request, 'email.html')
#     return HttpResponse('Mail successfully sent')


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


@login_required
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


@login_required
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


@login_required
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


@login_required
def edit_pet(request,pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = AddAPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect(to='home')
    else:
        form = AddAPetForm(instance=pet)

    context = {
        'form': form,
    }
    return render(request, 'edit_pet.html', context)



def profile_page(request,pk):
        user = Profile.objects.get(pk=pk)
        existing_contact = Contact.objects.filter(user=request.user).filter(name=user)
        user_contacts = Contact.objects.filter(user=request.user)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect(to='home')
        else:
            form = ProfileForm(instance=request.user.profile)

        
        
        return render(request, 'profile.html', {
        'user' : user,
        'existing_contact': existing_contact,
        'form': form,
        'user_contacts': user_contacts
 
        })


def contact_added(request,pk):
        user = User.objects.get(id=pk)
        contact_profile = Profile.objects.get(pk=pk)
        mainuser = request.user
        new_contact = Contact(user=mainuser, name=contact_profile.user.username, email=user.email)
        new_contact.save()
        pk = request.user.id
        return redirect(to='profile', pk=pk)


        return render(request, 'profile', {
        'contact_profile': contact_profile,
        'user': user,
 
        })


