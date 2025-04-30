from django.urls import path
from api.views import VacancyApiView, VacancyDetailView

urlpatterns = [
    path('vacancies/', VacancyApiView.as_view()),
    path('vacancy/<int:pk>/', VacancyDetailView.as_view()),
]