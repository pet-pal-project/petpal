from django.shortcuts import render
from core.models import Pet, Routine, Critical, Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

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

