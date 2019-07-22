from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users',views.AllUsers.as_view(), name='users-all'),
    path('annotations', views.AllAnnotations.as_view(), name='annotations-all')
    #path('') path for the filtered annotations
]

urlpatterns = format_suffix_patterns(urlpatterns)