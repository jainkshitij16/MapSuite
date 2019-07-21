from django.contrib import admin
from .models import Annotation,Userprofile
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Annotation)