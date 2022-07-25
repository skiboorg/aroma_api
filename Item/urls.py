from django.urls import path,include
from . import views

urlpatterns = [


    path('get/', views.GetItems.as_view()),

    path('one/', views.GetItem.as_view()),




]
