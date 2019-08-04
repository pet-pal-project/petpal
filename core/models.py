from django.db import models
import datetime, os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.

class Pet (models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    animal = models.CharField(max_length=150, null=False, blank=False)
    breed = models.CharField(max_length=150, null=False, blank=True)
    weight_in_lbs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sex = models.CharField(max_length=20, blank=True)
    color_and_Markings = models.CharField(max_length=200, blank=True)
    age = models.CharField(max_length=4, null=True, blank=True)
    profile_Image = models.ImageField(upload_to="pet_pictures", blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="pet_owner")
    about_Me = models.TextField(max_length=2000, help_text="Tell us about your pet (likes, dislikes, fun quirks, and more).", null=True, blank=True)
    vet_Info = models.TextField(max_length=2000, help_text="Enter your pet's vet info (name, address, and contact number).", null=True, blank=True)
    emergency_Contact = models.TextField(max_length=2000, help_text="Someone other than yourself in the case of emergencies (enter their name, number, and email).", null=True, blank=True)
    

    def image_path(instance, filename):
        return os.path.join('media', str(instance.id), filename)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pet-detail', args=[str(self.id)])

class Visit (models.Model):
    sitter_id = models.CharField(max_length=50, null=False, blank=False)
    due_date_on = models.DateTimeField(auto_now=False)        

class Checklist (models.Model):
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
    visits = models.ForeignKey(Visit, on_delete=models.CASCADE)


class Task (models.Model):
    description = models.TextField(null=False, blank=False)
    checklist_id = models.ForeignKey(Checklist, on_delete=models.SET_NULL, null=True) 
    completed = models.BooleanField(default=False)







    

# class Routine (models.Model):
#     description = models.TextField(max_length=200, null=False, blank=False)
#     due_date = models.DateTimeField()
#     assigned_pet = models.ForeignKey(to=Pet, on_delete=models.SET_NULL, null=True)
#     complete = models.BooleanField(default=False)
#     notes = models.TextField(max_length=2000, null=True, blank=True)
#     assigned_sitter = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="assigned_sitter")

#     def __str__(self):
#         return self.description

# class Critical (models.Model):
#     description = models.TextField(max_length=200, null=False, blank=False)
#     due_date = models.DateTimeField()
#     assigned_pet = models.ForeignKey(to=Pet, on_delete=models.SET_NULL, null=True)
#     complete = models.BooleanField(default=False)
#     notes = models.TextField(max_length=2000, null=True, blank=True)

#     def __str__(self):
#         return self.description

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, blank=False, help_text="Enter your first and last name")
    home_phone= models.CharField(max_length=10, blank=True)
    mobile_phone = models.CharField(max_length=10, blank=True)
    work_phone = models.CharField(max_length=10, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f"{self.user}"