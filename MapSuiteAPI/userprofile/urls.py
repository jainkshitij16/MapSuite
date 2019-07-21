from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',views.Allsers.as_View(), name='users-all')
]

urlpatterns = format_suffix_patterns(urlpatterns)