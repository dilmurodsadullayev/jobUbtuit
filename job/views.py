from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Vacancy, Document
from .forms import DocumentCreateForm
# Create your views here.

def index_view(request):
    vacancies = Vacancy.objects.all()

    ctx = {
        "vacancies": vacancies

    }

    return render(request, 'main/index.html', ctx)


def vacancy_detail(request,vacancy_id):
    if request.method == "GET":
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        try:
            document = Document.objects.get(vacancy=vacancy)
            education_levels = Document.EDUCATION_LEVELS
            form = DocumentCreateForm()
            ctx = {
                "vacancy": vacancy,
                "form": form,
                "education_levels": education_levels,
                "document": document
            }
            return render(request, "main/vacancy_detail.html", ctx)
        except:
            education_levels = Document.EDUCATION_LEVELS
            form = DocumentCreateForm()
            ctx = {
                "vacancy": vacancy,
                "form": form,
                "education_levels": education_levels,
            }
            return render(request, "main/vacancy_detail.html", ctx)


    elif request.method == "POST":
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        try:
            document = Document.objects.get(vacancy=vacancy)
            form = DocumentCreateForm(request.POST, request.FILES)
            education_levels = Document.EDUCATION_LEVELS

            if form.is_valid():
                document = form.save(commit=False)
                document.status = True
                document.save()
                return HttpResponse("Siz vacancy yubordingiz!")
            # else:
            #     print("Form is invalid:", form.errors)

            ctx = {
                "vacancy": vacancy,
                "form": form,
                "education_levels": education_levels,
                "document": document

            }
            return render(request, "main/vacancy_detail.html", ctx)

        except:
            form = DocumentCreateForm(request.POST, request.FILES)
            education_levels = Document.EDUCATION_LEVELS

            if form.is_valid():
                document = form.save(commit=False)
                document.status = True
                document.save()
                return HttpResponse("Siz vacancy yubordingiz!")
            # else:
            #     print("Form is invalid:", form.errors)

            ctx = {
                "vacancy": vacancy,
                "form": form,
                "education_levels": education_levels,


            }
            return render(request, "main/vacancy_detail.html", ctx)


def custom_404(request, exception):
    return render(request, '404.html', status=404)