from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Vacancy, Document, CustomUser, DocumentUser,DocumentIssue, View

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
    list_display = ('education_level', 'timestamp')
    list_filter = ('timestamp',)
    # search_fields = ('full_name',)
    ordering = ('-timestamp',)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'birthdate', 'middle_name', 'phone_number']
    search_fields = ['username', 'email']
    list_filter = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'middle_name', 'email', 'birthdate', 'phone_number')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'birthdate', 'middle_name', 'phone_number'),
        }),
    )


admin.site.register(CustomUser)
admin.site.register(DocumentIssue)
admin.site.register(DocumentUser)
admin.site.register(View)