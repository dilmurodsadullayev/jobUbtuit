from django.urls import path




from . import views


urlpatterns = [
    path('', views.index_view, name="home"),
    path('job/<int:vacancy_id>', views.vacancy_detail, name="vacancy_detail"),
    path('job/<int:vacancy_id>/success',views.success_view, name='success')

]

