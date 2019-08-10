from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    path('users',views.getAllUsers.as_view(), name='all-users'),
    path('usergroup=<str:community>', views.getAllUserswithCom.as_view(), name='com-users'),
    path('username=<str:username>/annotations=<str:keyword>', views.getSingleUserAnnotation.as_view(), name='user-singleannotation'),
    path('username=<str:username>/label=<str:label>',views.getUserLabel.as_view(), name='user-label'),
    path('username=<str:username>/annotations',views.getUserAnnotations.as_view(), name='user-annotations'),

    path('register_user', views.RegisterUser.as_view(), name='create-user'),
    path('add_annotation', views.RegisterAnnotation.as_view(), name='create-annotation'),

    path('annotations=<str:keyword>/users', views.getAnnotationUsers.as_view(), name='annotation-users'),
    path('annotations/search_location_name=<str:keyword>', views.getAnnotionfromKeyword.as_view(), name='keyword-annotation'),
    path('annotations/search_text=<str:keyword>', views.getAnnotationwithTextKeyword.as_view(), name='intext-annotations'),
    path('annotations/usergroup=<str:community>', views.getAnnotationsofCommunity.as_view(), name='com-annotations'),
    path('annotations', views.getAllAnnotations.as_view(), name='all-annotations'),

    path('<str:username>/join_community', views.JoinCommunity.as_view(), name='join_community'),
    path('add_community', views.RegisterCommunity.as_view(), name='create-community'),
    path('communities', views.getcomm.as_view(), name='communities-all'),

    path('<str:model>/object_change/<int:pk>', views.ObjectChange.as_view(), name='object-change'),

]

urlpatterns = format_suffix_patterns(urlpatterns)