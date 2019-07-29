from django.contrib import admin
from core.models import Pet, Routine, Critical, Profile

admin.site.register(Pet)
admin.site.register(Routine)
admin.site.register(Critical)
admin.site.register(Profile)