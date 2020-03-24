

from django.urls import path,re_path
from apps.user import views

urlpatterns = [
    re_path('^register',views.register,name='register')
]
