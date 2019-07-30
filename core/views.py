from django.shortcuts import render
from core.models import Pet, Routine, Critical, Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    pet_list = Pet.objects.all()

    context = {
        'pet_list': pet_list,
    }
    return render(request, 'dashboard.html', context=context)