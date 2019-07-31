from django.contrib import admin
from core.models import Pet, Visit, Checklist, Task, Profile

admin.site.register(Pet)
admin.site.register(Visit)
admin.site.register(Checklist)
admin.site.register(Task)
admin.site.register(Profile)