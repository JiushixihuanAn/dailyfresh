from apps.goods import views

from django.urls import re_path,path
app_name = 'goods'
urlpatterns = [
    path('',views.index,name='index'),
]
