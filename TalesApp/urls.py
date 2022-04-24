from django.urls import path,include
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('load_tale',views.LoadTale,name='load'),
    path('comment/<int:pk>',views.comment,name='comment'),
    path('reply/<int:pk>',views.reply,name='reply'),
    path('mark/<int:pk>',views.mark,name='mark'),
    path('story_<int:pk>',views.TaleView.as_view(),name='tale'),
    path('query=<str:query>',views.search_result,name='list'),
    path('genre/<str:title>',views.TaleList.as_view(),name='list'),
    path('genre/<str:title>/<int:pg>',views.TaleList.as_view(),name='list'),
    ]
