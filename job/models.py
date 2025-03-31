from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
import re
import os
from django.core.files.storage import default_storage

# Create your models here.

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

        # if self.opening_time < self.end_time:
        #     raise ValidationError("End date boshlanish sanasidan oldin bo'lishi mumkin emas!")

    def __str__(self):
        return f"{self.position} {'Muddati tugagan ' if self.status else 'Muddati hali tugamadi'}"


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


def validate_phone_number(value):
    # Telefon raqam faqat raqamlardan va + belgisidan iborat ekanligini tekshiramiz
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError("Telefon raqam +998 bilan boshlanishi va jami 13 ta belgidan iborat bo'lishi kerak.")


def validate_image_or_pdf(file):
    # Ruxsat berilgan fayl kengaytmalari
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = os.path.splitext(file.name)[1].lower()  # Fayl kengaytmasini olish
    if ext not in valid_extensions:
        raise ValidationError(f"Faqat quyidagi formatlardagi fayllar yuklanishi mumkin: {', '.join(valid_extensions)}.")

    # Maksimal fayl hajmini tekshirish (masalan, 5 MB)
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
    vacancy = models.ForeignKey(Vacancy,on_delete=models.SET_NULL, null=True,blank=True)
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField(validators=[validate_birth_date])
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
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
    status = models.BooleanField(default=False)

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
        return  f"{self.full_name} : {'Ariza Yuborgan' if self.status else 'Yuborilmagan'}"