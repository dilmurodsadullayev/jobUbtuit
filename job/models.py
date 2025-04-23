from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
import re
import os
from django.core.files.storage import default_storage

# Create your models here.

def validate_birth_date(value):
    today = date.today()
    min_age = 18
    max_age = 120

    if value > today:
        raise ValidationError("Tug'ilgan sana kelajakdagi sana bo'lishi mumkin emas.")
    elif (today - value).days // 365 < min_age:
        raise ValidationError(f"Tug'ilgan sana bo'yicha foydalanuvchi kamida {min_age} yoshda bo'lishi kerak.")
    elif (today - value).days // 365 > max_age:
        raise ValidationError(f"Tug'ilgan sana bo'yicha foydalanuvchi {max_age} yoshdan katta bo'lishi mumkin emas.")

class CustomUser(AbstractUser):
    birthdate = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True, region="UZ")

    def clean(self):
        super().clean()

        if self.birthdate > date.today():
            raise ValidationError("Tug'ilgan sana kelajakda bo'lishi mumkin emas.")

        min_age = 18
        age = date.today().year - self.birthdate.year
        if (date.today().month, date.today().day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        if age < min_age:
            raise ValidationError(f"Yosh kamida {min_age} yosh bo'lishi kerak.")



# class Vacancy(models.Model):
#     position_uz = models.CharField(max_length=50) # lavozim
#     position_eng = models.CharField(max_length=50) # lavozim
#     position_ru = models.CharField(max_length=50) # lavozim
#
#     department_uz = models.CharField(max_length=50) # bo'lim
#     department_eng = models.CharField(max_length=50) # bo'lim
#     department_ru = models.CharField(max_length=50) # bo'lim
#
#     rate_uz = models.CharField(max_length=50) # daraja
#     rate_eng = models.CharField(max_length=50) # daraja
#     rate_ru = models.CharField(max_length=50) # daraja
#
#     salary_uz = models.CharField(max_length=50)
#     salary_eng = models.CharField(max_length=50)
#     salary_ru = models.CharField(max_length=50)
#
#     experience_uz = models.CharField(max_length=50,null=True,blank=True) # tajriba
#     experience_eng = models.CharField(max_length=50,null=True,blank=True) # tajriba
#     experience_ru = models.CharField(max_length=50,null=True,blank=True) # tajriba
#
#     work_schedule_uz = models.CharField(max_length=50) # ish grafigi
#     work_schedule_eng = models.CharField(max_length=50) # ish grafigi
#     work_schedule_ru = models.CharField(max_length=50) # ish grafigi
#
#     requirement_uz = models.CharField(max_length=150) # talablar
#     requirement_eng = models.CharField(max_length=150) # talablar
#     requirement_ru = models.CharField(max_length=150) # talablar
#
#     opening_time = models.DateField(default=date.today)
#     end_time = models.DateField()
#     status = models.BooleanField(default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def clean(self):
#         """ Ma'lumotlarni validatsiya qilish """
#         if self.end_time and self.end_time < self.opening_time:
#             raise ValidationError({'end_time': "Tugash vaqti ochilish vaqtidan oldin bo‘lishi mumkin emas!"})
#
#     def save(self, *args, **kwargs):
#         """ Ma'lumotlarni saqlashdan oldin statusni yangilash """
#         if self.end_time and self.end_time < date.today():
#             self.status = False
#         else:
#             self.status = True
#         super().save(*args, **kwargs)
class Vacancy(models.Model):
    position = models.CharField(max_length=50) # lavozim
    department = models.CharField(max_length=50) # bo'lim
    rate = models.CharField(max_length=50) # daraja
    salary = models.CharField(max_length=50)
    experience = models.CharField(max_length=50,null=True,blank=True) # tajriba
    work_schedule = models.CharField(max_length=50) # ish grafigi
    requirement = models.CharField(max_length=150) # talablar
    opening_time = models.DateField(default=date.today)
    end_time = models.DateField()
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Agar end_time opening_time dan oldin bo‘lsa xato chiqaramiz
        if self.end_time < self.opening_time:
            raise ValidationError({'end_time': "Tugash vaqti ochilish vaqtidan oldin bo‘lishi mumkin emas!"})

        # Agar sanalar hozirgi kundan o‘tgan bo‘lsa, statusni `False` qilamiz
        if self.end_time < date.today():
            self.status = False
        else:
            self.status = True


    def __str__(self):
        return f"{self.position} {'Muddati tugagan ' if self.status else 'Muddati hali tugamadi'}"








def validate_image_or_pdf(file):
    # Ruxsat berilgan fayl kengaytmalari
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = os.path.splitext(file.name)[1].lower()  # Fayl kengaytmasini olish
    if ext not in valid_extensions:
        raise ValidationError(f"Faqat quyidagi formatlardagi fayllar yuklanishi mumkin: {', '.join(valid_extensions)}.")

    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
        raise ValidationError("Fayl hajmi 5 MB dan oshmasligi kerak.")

EDUCATION_LEVELS = (
        ("o'rta", "O'rta"),
        ("o'rta maxsus", "O'rta maxsus"),
        ("bakalavr", "Bakalavr"),
        ("magistr", "Magistr"),
    )

def validate_status(value):
    valid_choices = [choice[0] for choice in EDUCATION_LEVELS]
    if value not in valid_choices:
        raise ValidationError(f"Status '{value}' noto‘g‘ri. Faqat {valid_choices} qabul qilinadi.")


class Document(models.Model):
    EDUCATION_LEVELS = (
        ("o'rta", "O'rta"),
        ("o'rta maxsus", "O'rta maxsus"),
        ("bakalavr", "Bakalavr"),
        ("magistr", "Magistr"),
    )
    DOCUMENT_STATUS = [
        ('submitted', 'Submitted'),
        ('under review', 'Under review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    vacancy = models.ForeignKey(Vacancy,on_delete=models.SET_NULL, null=True,blank=True)
    education_level = models.CharField(
        max_length=15,
        choices=EDUCATION_LEVELS,
        default="O'rta",
        validators=[validate_status],
    )
    passport = models.FileField(
        upload_to='documents/',
        validators=[validate_image_or_pdf],
    )
    objective = models.FileField(
        upload_to='documents/',
        validators=[validate_image_or_pdf],
    )
    diploma = models.FileField(
        upload_to='documents/',
        validators=[validate_image_or_pdf],
        )

    language_certificate = models.FileField(
        upload_to='documents/',
        validators=[validate_image_or_pdf],
    )

    benefits = models.FileField(
        upload_to='documents/',
        validators=[validate_image_or_pdf],
    )
    status = models.CharField(max_length=50,choices=DOCUMENT_STATUS,default='submitted')
    # status = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """
        Model o‘chirilar ekan, unga bog‘langan barcha fayllarni ham media papkadan o‘chiradi.
        """
        file_fields = [self.passport, self.objective, self.diploma, self.language_certificate, self.benefits]

        for file_field in file_fields:
            if file_field and file_field.path and os.path.isfile(file_field.path):
                os.remove(file_field.path)

        super().delete(*args, **kwargs)



    def __str__(self):
        return  f"{self.education_level}"



class DocumentUser(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    document = models.ForeignKey(Document,on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.user.username)} {self.document}"


class View(models.Model):
    user = models.ForeignKey(CustomUser,null=True, blank=True, on_delete=models.SET_NULL)
    vacancy = models.ForeignKey(Vacancy,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{str(self.user.username)} {str(self.vacancy)}"


class DocumentIssue(models.Model):
    document_user = models.ForeignKey(DocumentUser, on_delete=models.CASCADE)
    message = models.TextField()  # Kamchilik matni
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)  # Hal qilindimi yoki yo‘q

    def __str__(self):
        return f"Kamchilik: {self.message[:30]}"