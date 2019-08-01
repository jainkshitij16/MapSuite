from django.contrib import admin
from .models import Annotation,Userprofile, Story, Community
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Annotation)
admin.site.register(Community)
admin.site.register(Story)