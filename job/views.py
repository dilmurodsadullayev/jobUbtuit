from logging import exception
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vacancy, Document, DocumentUser, CustomUser, DocumentIssue, View
from .forms import DocumentCreateForm, RegistrationForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def index_view(request):
    vacancy_views_list = []

    for vacancy in Vacancy.objects.all():
        views_count = View.objects.filter(vacancy=vacancy).count()
        vacancy_views_list.append({
            'vacancy': vacancy,
            'views': views_count
        })



    ctx = {
        "vacancy_views_list": vacancy_views_list

    }

    return render(request, 'main/index.html', ctx)

@login_required(login_url="/signin")
def vacancy_detail(request,vacancy_id):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "GET":
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        is_view = View.objects.filter(user=user, vacancy=vacancy).exists()
        document_count = Document.objects.filter(vacancy=vacancy).count()
        if not is_view:
            View.objects.create(user=user, vacancy=vacancy)
        else:
            pass

        try:
            document = Document.objects.get(vacancy=vacancy)
            education_levels = Document.EDUCATION_LEVELS
            form = DocumentCreateForm()
            ctx = {
                "vacancy": vacancy,
                'document_count': document_count,
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
                'document_count': document_count,
                "form": form,
                "education_levels": education_levels,
            }
            return render(request, "main/vacancy_detail.html", ctx)


    elif request.method == "POST":
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        try:
            vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
            document = Document.objects.get(vacancy=vacancy)
            form = DocumentCreateForm(request.POST, request.FILES)
            education_levels = Document.EDUCATION_LEVELS

            if form.is_valid():
                document = form.save(commit=False)
                document.save()
                # print(document)
                DocumentUser.objects.create(
                    user=user,
                    document=document
                )

                return redirect("success", vacancy_id=vacancy.id)
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

                document.save()
                print(document)
                DocumentUser.objects.create(
                    user=user,
                    document=document
                )
                # return HttpResponse("Siz vacancy yubordingiz!")
                return redirect("success", vacancy_id=vacancy.id)
            # else:
            #     print("Form is invalid:", form.errors)

            ctx = {
                "vacancy": vacancy,
                "form": form,
                "education_levels": education_levels,


            }
            return render(request, "main/vacancy_detail.html", ctx)



def success_view(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    document_status = Document.objects.filter(vacancy=vacancy).first()

    ctx = {
        "document_status": document_status,
        "vacancy": vacancy,
    }

    return render(request, "main/success.html", ctx)


def my_application(request):
    user = CustomUser.objects.get(id=request.user.id)
    my_applications = DocumentUser.objects.filter(user=user)
    ctx = {
        "my_applications": my_applications
    }

    return render(request, 'main/my_application.html', ctx)


def hover_status(request):
    document_id = request.GET.get('id')  # GET orqali kelgan document_id
    if document_id:
        try:
            # Shu document_id bo‘yicha DocumentUserni topamiz
            document_user = DocumentUser.objects.get(document=document_id)

            # DocumentIssue larni olib chiqamiz
            issue = DocumentIssue.objects.filter(document_user__document=document_user.document).first()

            # Agar issues bo'lsa, ularni chiqaramiz
            if issue:
                issues_data = [
                    {
                        "id": issue.id,
                        "message": issue.message,
                        "resolved": issue.resolved,
                        "created_at": issue.created_at.strftime("%Y-%m-%d %H:%M"),
                    }
                ]
                return JsonResponse({'issues': issues_data})
            else:
                return JsonResponse({'message': 'Hech qanday kamchilik topilmadi.'})

        except DocumentUser.DoesNotExist:
            return JsonResponse({'message': 'DocumentUser topilmadi'}, status=404)





def signup_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Ma'lumotlaringizni to'g'ri kiriting.")  # Umumiy xato xabari
    else:
        form = RegistrationForm()

    ctx = {
        "form": form
    }

    return render(request, 'registration/sign_up.html', ctx)

def sign_in_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Foydalanuvchini tizimga kiritamiz
                return redirect('home')  # Bosh sahifaga yo'naltirish
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/sign_in.html', {'form': form})

@login_required(login_url="/signin")
def profile_view(request):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=user)  # 🔥 instance=user qo'shildi!

        if form.is_valid():
            updated_user = form.save(commit=False)  # Faylasuflik: commit=False qilsang, o'zing set qilasan

            # 🔎 Tekshiramiz: qaysi maydonlar POST'da borligini
            if request.POST.get('username'):
                updated_user.username = request.POST.get('username')
            if request.POST.get('fname'):
                updated_user.first_name = request.POST.get('first_name')
            if request.POST.get('lname'):
                updated_user.last_name = request.POST.get('last_name')
            if request.POST.get('email'):
                updated_user.email = request.POST.get('email')
            if request.POST.get('birthdate'):
                updated_user.birthdate = request.POST.get('birthdate')
            if request.POST.get('phone'):
                updated_user.phone_number = request.POST.get('phone_number')

            # 🔐 Parollarni tekshirish (agar kiritsa)
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 and password2:
                if password1 == password2:
                    updated_user.set_password(password1)
                else:
                    messages.error(request, "Parollar mos kelmayapti!")

            updated_user.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi ✅")
            return redirect('profile')  # Profil sahifasiga qaytaramiz

        else:
            messages.error(request, "Xatoliklar yuz berdi, iltimos tekshirib qayta yuboring.")
            print(form.errors)
    else:
        form = RegistrationForm(instance=user)

    ctx = {
        'form': form,
        'user': user,
    }
    return render(request, 'main/profile.html', ctx)


def custom_404(request, exception):
    return render(request, '404.html', status=404)





def logout_view(request):
    logout(request)  # Foydalanuvchini tizimdan chiqarish
    return redirect('home')