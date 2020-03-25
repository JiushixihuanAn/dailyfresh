

from django.urls import path,re_path
from apps.user import views

urlpatterns = [
    re_path('^register',views.register,name='register'),
    path('register_handle',views.register_handle,name='register_handle'),


]
