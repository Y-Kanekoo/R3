# 修正例
from django.shortcuts import render, redirect, get_object_or_404  # Djangoのインポートは先に行う
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import generics  # 外部ライブラリのインポート

from .models import Employee, Questionnaire, DailyReport, DailyReportAnswer, QuestionnaireThreshold, QuestionnaireOption
from .serializers import EmployeesSerializer, QuestionnairesSerializer, DailyReportsSerializer, DailyReportAnswersSerializer
from myapp.forms.signup import SignUpForm  # 最後にアプリ関連のインポートを行う



def profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST["email"]
        user.username = request.POST["username"]
        user.save()
        return redirect("profile")
    else:
        return render(request, "accounts/profile.html")




class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("profile")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())

User = get_user_model()
@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@staff_member_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return redirect('accounts/user_list')

    return render(request, 'accounts/user_list.html')