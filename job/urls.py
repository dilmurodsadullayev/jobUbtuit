from django.urls import path




from . import views


urlpatterns = [
    path('', views.index_view, name="home"),
    path('vacancy/<int:vacancy_id>', views.vacancy_detail, name="vacancy_detail"),

]

