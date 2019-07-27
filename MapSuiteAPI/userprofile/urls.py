from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('users/<int:pk>', views.RetreiveUser.as_view(), name='one-user'),
    path('annotations/<int:pk>', views.RetreiveAnnotation.as_view(), name='one-annotation'),
    path('users',views.AllUsers.as_view(), name='all-users'),
    path('annotations', views.AllAnnotations.as_view(), name='all-annotations'),
    path('testing/<str:username>',views.UserwithAnnotations.as_view(), name='testing')

    #path('<str:agent>/<int:pk>', views.RetrieveAgent.as_view(), name='one-agent'),
    #path('') path for the filtered annotations
]

urlpatterns = format_suffix_patterns(urlpatterns)