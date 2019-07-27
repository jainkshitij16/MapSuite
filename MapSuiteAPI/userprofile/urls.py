from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('users/<int:pk>', views.RetreiveUser.as_view(), name='one-user'),
    path('annotations/<int:pk>', views.RetreiveAnnotation.as_view(), name='one-annotation'),
    path('annotations=<str:keyword>/users', views.getAnnotationUsers.as_view(), name='annotation-users'),
    path('annotations=<str:keyword>', views.getAnnotionfromKeyword.as_view(), name='keyword-annotation'),
    path('annotations/search_text=<keyword>', views.getAnnotationwithTextKeyword.as_view(), name='intext-annotations'),
    path('usergroup=<str:group>', views.getAllUserswithCat.as_view(), name='cat-users'),
    path('users',views.getAllUsers.as_view(), name='all-users'),
    path('annotations', views.getAllAnnotations.as_view(), name='all-annotations'),
    path('username=<str:username>/annotations=<str:keyword>', views.getSingleUserAnnotation.as_view(), name='user-singleannotation'),
    path('username=<str:username>/annotations/home',views.getUserHomes.as_view(), name='user-homes'),
    path('username=<str:username>/annotations',views.getUserAnnotations.as_view(), name='user-annotations'),

    #path('<str:agent>/<int:pk>', views.RetrieveAgent.as_view(), name='one-agent'),
    #path('') path for the filtered annotations
]

urlpatterns = format_suffix_patterns(urlpatterns)