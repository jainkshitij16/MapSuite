from django.contrib import admin
from .models import Location,Userprofile
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Location)