from rest_framework import serializers
from job.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            'id',
            'position',
            'department',
            'rate',
            'salary',
            'experience',
            'work_schedule',
            'requirement',
            'opening_time',
            'end_time',
            'status',
        ]