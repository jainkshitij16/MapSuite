from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('users/<int:pk>', views.RetreiveUser.as_view(), name='one-user'),
    path('users',views.getAllUsers.as_view(), name='all-users'),
    path('usergroup=<str:community>', views.getAllUserswithCom.as_view(), name='com-users'),
    path('username=<str:username>/annotations=<str:keyword>', views.getSingleUserAnnotation.as_view(), name='user-singleannotation'),
    path('username=<str:username>/label=<str:label>',views.getUserLabel.as_view(), name='user-label'),
    path('username=<str:username>/annotations',views.getUserAnnotations.as_view(), name='user-annotations'),

    path('user', views.RegisterUser.as_view(), name='create-user'),
    path('annotation', views.RegisterAnnotation.as_view(), name='create-annotation'),

    path('annotations/<int:pk>', views.RetreiveAnnotation.as_view(), name='one-annotation'),
    path('annotations=<str:keyword>/users', views.getAnnotationUsers.as_view(), name='annotation-users'),
    path('annotations=<str:keyword>', views.getAnnotionfromKeyword.as_view(), name='keyword-annotation'),
    path('annotations/search_text=<str:keyword>', views.getAnnotationwithTextKeyword.as_view(), name='intext-annotations'),
    path('annotations/usergroup=<str:community>', views.getAnnotationsofCommunity.as_view(), name='com-annotations'),
    path('annotations', views.getAllAnnotations.as_view(), name='all-annotations'),
    path('test', views.getcomm.as_view()) #TODO: update this


    #path('<str:agent>/<int:pk>', views.RetrieveAgent.as_view(), name='one-agent'),
    #path('') path for the filtered annotations
]

urlpatterns = format_suffix_patterns(urlpatterns)