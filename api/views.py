from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from job.models import Vacancy
from .serializers import VacancySerializer
from rest_framework.views import APIView


# Create your views here.

class VacancyApiView(APIView):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data)



class VacancyDetailView(APIView):

    def get(self, request, pk):
        vacancy = get_object_or_404(Vacancy, pk=pk)
        serializer = VacancySerializer(vacancy, many=False)
        return Response(serializer.data)