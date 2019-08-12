from django.shortcuts import render, redirect, get_object_or_404
from core.models import Pet, Visit, Checklist, Task, Profile, Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from core.forms import ProfileUpdateForm, ProfileForm, ChecklistForm, AddAPetForm, UserForm, ChecklistForm2, ProfileSearch
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from twilio.rest import Client
from django.views.generic import TemplateView
from django.contrib import messages
import os
import environ
import datetime


# Create your views here.  


@login_required
def index(request):
    my_pet_list = Pet.objects.filter(owner=request.user)
    my_visits = Visit.objects.filter(sitter_id=request.user).order_by('due_date_on')
    all_pets = Pet.objects.all()
    if my_visits:
        next_visit = my_visits[0]

    all_checklists = Checklist.objects.all()
    all_tasks = Task.objects.all()
    all_pets = Pet.objects.all()
    checked_pets=[]
    unique_visits=[]
    result_visits=[]

    for visit in my_visits:
        for checklist in all_checklists:
            if checklist.visit == visit:
                if checklist.pet_id not in checked_pets and visit not in unique_visits:
                    unique_visits.append(visit)
                    checked_pets.append(checklist.pet_id)
                    print(checklist.pet_id)
                    print(visit)

                            
    result_visits.append(checked_pets)
    result_visits.append(unique_visits)

    print(result_visits)
    if request.method == 'POST' and 'delete-checklist' in request.POST:
        id_num = request.POST.get('delete-checklist')
        Checklist.objects.get(id=id_num).delete()
        messages.success(request, 'Checklist successfuly deleted')
        return redirect('home')


    context = {
        'my_pet_list': my_pet_list,
        'my_visits': my_visits,
        'all_checklists': all_checklists,
        'all_tasks': all_tasks,
        'unique_visits': unique_visits,
        'all_pets': all_pets,
        'checked_pets': checked_pets,
        'result_visits': result_visits,

    }
    return render(request, 'dashboard.html', context=context)


@login_required
def pet_detail(request,pk):
    my_pet_list = Pet.objects.filter(owner=request.user)
    pet = Pet.objects.get(pk=pk)
    owner = Profile.objects.get(user=pet.owner)
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
        checklist_sumbitted_notification(request, user, tasks)

        if tasks_checked:
            account_sid = os.environ.get('account_sid')
            auth_token = os.environ.get('auth_token')
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                    body=f"Hi { pet.owner }, { pet.name }'s checklist has been submitted! Login to your account to view the details: http://www.crittersitterapp.com", 
                    from_='+19842144116',
                    to=f'{ owner.phone }',
                )

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
        form = ChecklistForm2(request.POST)
        sitterform = UserForm(request.POST, user=request.user)
        if form.is_valid() and sitterform.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            sitter = sitterform.cleaned_data.get('sitter') 
            task1 = request.POST['task1']
            task2 = request.POST['task2']
            task3 = request.POST['task3']
            task4 = request.POST['task4']
            task5 = request.POST['task5']
            task6 = request.POST['task6']
            task7 = request.POST['task7']
            task8 = request.POST['task8']
            task9 = request.POST['task9']
            task10 = request.POST['task10']
            print (start_date)
            print (end_date)
            delta = end_date - start_date
            print(delta.days)
            existing_visit = Visit.objects.filter(sitter_id=sitter).filter(due_date_on=start_date)
            num_of_days = delta.days
            if delta.days == 0:
                if existing_visit:
                    visitpk = existing_visit[0]
                    Checklist.objects
                    existing_checklist = Checklist.objects.filter(visit=visitpk).filter(pet_id=pet)
                    
                    if existing_checklist:
                        checklist = existing_checklist[0]
                    else:
                        checklist = Checklist(visit=visitpk, pet_id=pet)
                        checklist.save()

                    if task1:
                        new_task1 = Task(description=task1, checklist_id=checklist)
                        new_task1.save()
                    if task2:
                        new_task2 = Task(description=task2, checklist_id=checklist)
                        new_task2.save()
                    if task3:
                        new_task3 = Task(description=task3, checklist_id=checklist)
                        new_task3.save()
                    if task4:
                        new_task4 = Task(description=task4, checklist_id=checklist)
                        new_task4.save()
                    if task5:
                        new_task5 = Task(description=task5, checklist_id=checklist)
                        new_task5.save()
                    if task6:
                        new_task6 = Task(description=task6, checklist_id=checklist)
                        new_task6.save()
                    if task7:
                        new_task7 = Task(description=task7, checklist_id=checklist)
                        new_task7.save()
                    if task8:
                        new_task8 = Task(description=task8, checklist_id=checklist)
                        new_task8.save()
                    if task9:
                        new_task9 = Task(description=task9, checklist_id=checklist)
                        new_task9.save()
                    if task10:
                        new_task10 = Task(description=task10, checklist_id=checklist)
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
                    print(current_date)
                    existing_visit = Visit.objects.filter(sitter_id=sitter).filter(due_date_on=current_date)
                
                    if existing_visit:
                        print("EXISTING VISIT")
                        visitpk = existing_visit[0]
                        print(visitpk)
                        Checklist.objects
                        existing_checklist = Checklist.objects.filter(visit=visitpk).filter(pet_id=pet)

                        if existing_checklist:
                            checklist = existing_checklist[0]
                        else:
                            checklist = Checklist(visit=visitpk, pet_id=pet)
                            checklist.save()

                        if task1:
                            new_task1 = Task(description=task1, checklist_id=checklist)
                            new_task1.save()
                        if task2:
                            new_task2 = Task(description=task2, checklist_id=checklist)
                            new_task2.save()
                        if task3:
                            new_task3 = Task(description=task3, checklist_id=checklist)
                            new_task3.save()
                        if task4:
                            new_task4 = Task(description=task4, checklist_id=checklist)
                            new_task4.save()
                        if task5:
                            new_task5 = Task(description=task5, checklist_id=checklist)
                            new_task5.save()
                        if task6:
                            new_task6 = Task(description=task6, checklist_id=checklist)
                            new_task6.save()
                        if task7:
                            new_task7 = Task(description=task7, checklist_id=checklist)
                            new_task7.save()
                        if task8:
                            new_task8 = Task(description=task8, checklist_id=checklist)
                            new_task8.save()
                        if task9:
                            new_task9 = Task(description=task9, checklist_id=checklist)
                            new_task9.save()
                        if task10:
                            new_task10 = Task(description=task10, checklist_id=checklist)
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
        form = ChecklistForm2()
        sitterform = UserForm(user=request.user)

        
    return render(request, 'add_checklist.html', {'form': form, 'pet' : pet, 'sitterform': sitterform})



# def new_pet_notification(request, user):
#     send_mail(
#         'You have created a new animal profile.',
#         f'Hi { user.username }, we are notifiying you that you have successfully created a new animal profile!',
#         'admin@critter-sitter.com',
#         [f'{ user.email }'],
#         fail_silently=False,
#     )
#     return render(request, 'email.html')
#     return HttpResponse('Mail successfully sent')



""" Notification to Owner that the Sitter has submitted a checklist."""
def checklist_sumbitted_notification(request, user, tasks):
    tasks = tasks
    send_mail(
        'Visit for today marked complete.',
         f'Hi { user.username }, we are notifiying you that your sitter has submitted their checklist for today. Log in to your account here to view the details: http://www.crittersitterapp.com/accounts/login/', 
        'admin@critter-sitter.com',
        [f'{ user.email }'],
        fail_silently=False,
    )
    return render(request, 'email.html')
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
            # new_pet_notification(request, user)
            # print("email sent")

            new_pet = form.save(commit=False)
            new_pet.owner = request.user
            new_pet.save()

            return redirect("home")
    else:
        form = AddAPetForm()
    return render(request, 'add_pet.html', {'form': form})  



@login_required
def profile_page(request,pk):
        user = Profile.objects.get(pk=pk)
        existing_contact = Contact.objects.filter(user=request.user).filter(name=user)
        user_contacts = Contact.objects.filter(user=request.user)

        if request.method == 'POST' and 'save-profile' in request.POST:
            form = ProfileForm(request.POST, instance=request.user.profile)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile was updated successfully!')
                pk = request.user.id
                return redirect(to='profile', pk=pk)

        if request.method == 'POST' and 'search-contact' in request.POST:
            search_user_form = ProfileSearch(request.POST)

            if search_user_form.is_valid():
                search_name = search_user_form.cleaned_data.get('user_search')
                search_filter = User.objects.filter(username=search_name)
                if search_filter:
                    user_pk=search_filter[0].pk
                    return redirect(to='profile', pk=user_pk)
                else:
                    messages.info(request, 'Profile not found')
                    return redirect(to='profile', pk=pk)


        else:
            form = ProfileForm(instance=request.user.profile)
            search_user_form = ProfileSearch()
        
        
        return render(request, 'profile.html', {
        'user' : user,
        'existing_contact': existing_contact,
        'form': form,
        'search_user_form': search_user_form,
        'user_contacts': user_contacts,
 
        })

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
        'pet': pet,
    }
    return render(request, 'edit_pet.html', context)




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


@login_required
def delete_pet(request,pk):
    pet = get_object_or_404(Pet, pk=pk)
    name = pet.name
    if request.method == 'POST':
        existing_visits = Checklist.objects.filter(pet_id=pet)
        for existing_visit in existing_visits:
            select_visit = existing_visit.visit
            Visit.objects.filter(id=select_visit.pk).delete()
        Pet.objects.filter(name=pet.name).delete()
        messages.success(request, 'Critter profile has been removed')
        return redirect(to='home')
  
    context = {
       'pet': pet,
    }
    return render(request, 'delete-pet.html', context)

@login_required
def delete_account(request,pk):
    user = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        user_id = User.objects.get(pk=pk)
        pets = Pet.objects.filter(owner=request.user)
        for pet in pets:
            existing_visits = Checklist.objects.filter(pet_id=pet)
            for existing_visit in existing_visits:
                select_visit = existing_visit.visit
                Visit.objects.filter(id=select_visit.pk).delete()
        User.objects.filter(id=user_id.pk).delete()
        return redirect(to='/accounts/login')
  
    context = {
       'user': user,
    }
    return render(request, 'delete-account.html', context)


