from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login' ), name='logout'),
    path('register/', Registerpage.as_view(), name= 'register'),
    path('', taskList.as_view(), name='tasks'),
    path('task/<int:pk>/', taskDetail.as_view(), name='task'),
    path('task_create/',taskCreate.as_view(), name="task_create" ),
    path('task_update/<int:pk>/', taskUpdate.as_view(), name="task_update" ),
    path('task_delete/<int:pk>/', taskDelete.as_view(), name="task_delete" )

]