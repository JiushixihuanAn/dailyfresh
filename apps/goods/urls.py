from goods import views

from django.urls import re_path,path

urlpatterns = [
    re_path(r'^$',views.index,name='index')
]
