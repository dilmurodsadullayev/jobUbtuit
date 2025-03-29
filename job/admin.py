from django.contrib import admin
from .models import Vacancy, Document

# Vacancy modeli uchun admin sozlamasi
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('position', 'department', 'opening_time', 'end_time', 'status', )
    list_filter = ('position', 'department', 'opening_time',"end_time",)
    search_fields = ('position', 'department',)
    ordering = ('-opening_time',)
    list_editable = ('status',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'education_level', "status", 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('full_name',)
    ordering = ('-timestamp',)
