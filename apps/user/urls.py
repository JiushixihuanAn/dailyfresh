
from apps.user.views import  RegisterView,ActiveView,LoginView
from django.urls import path,re_path
from apps.user import views
app_name = 'user'

urlpatterns = [
    # re_path('^register',views.register,name='register'),
#    path('register_handle',views.register_handle,name='register_handle'),
    path('register',RegisterView.as_view(),name='register'),
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),
    path('login',LoginView.as_view(),name='login'),

]
