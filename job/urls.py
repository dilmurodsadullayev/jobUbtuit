from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index_view, name="home"),
    path('job/<int:vacancy_id>', views.vacancy_detail, name="vacancy_detail"),
    path('job/<int:vacancy_id>/success',views.success_view, name='success'),
    path('my',views.my_application, name='my_application'),
    path('signup',views.signup_view, name='signup'),
    path('signin',views.sign_in_view, name='signin'),
    path('logout', LogoutView.as_view(), name='logout'),
path('hover-status/', views.hover_status, name='hover_status'),

]

