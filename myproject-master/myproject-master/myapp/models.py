
# myapp/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin,)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        # 'employee_type' フィールドを渡す
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # 'employee_type' を 'admin' に設定
        extra_fields.setdefault("employee_type", "admin")  
        extra_fields.setdefault("is_superuser", True)  # 'is_superuser' は PermissionsMixin に必要
        extra_fields.setdefault("is_active", True)  # 'is_active' も必要
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    employee_type = models.CharField(
        max_length=10,
        choices=[('admin', 'Admin'), ('general', 'General')],
        default='general'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        # Userモデルのデータを保存する前にEmployeeモデルの共通データを保存
        super().save(*args, **kwargs)

        # Employeeに共通データを保存
        if not hasattr(self, 'employee'):
            Employee.objects.create(
                user=self,
                employee_type=self.employee_type,  # Userのemployee_typeをEmployeeにコピー
            )

    class Meta:
        db_table = 'myapp_user'  # この行でテーブル名を指定


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    employee_type = models.CharField(
        max_length=10, choices=[('admin', 'Admin'), ('general', 'General')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # `Employee` が保存される際に `User` の `username` を `name` にコピーする
        if not self.name:  # `name` がまだ設定されていない場合
            self.name = self.user.username  # Userのusernameをnameにコピー
        if not self.employee_type:  # `employee_type` が設定されていない場合
            self.employee_type = self.user.employee_type  # Userのemployee_typeをコピー
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DailyReportMorning(models.Model):
    name = models.CharField(max_length=255)
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    sleep_quality = models.CharField(max_length=150)
    had_dinner_yesterday = models.CharField(max_length=10)
    had_breakfast_today = models.CharField(max_length=10)
    medicine_time = models.CharField(max_length=10)
    current_condition = models.CharField(max_length=10)
    current_condition_other = models.TextField(blank=True, null=True)
    anxiety_level = models.CharField(max_length=10)
    current_emotion = models.CharField(max_length=10)
    communication_willingness = models.CharField(max_length=10)
    physical_condition = models.CharField(max_length=10)
    concentration_level = models.CharField(max_length=10)
    physical_discomfort = models.CharField(max_length=10)
    self_esteem = models.CharField(max_length=10)
    willingness_to_depend = models.CharField(max_length=10)
    feeling_needed = models.CharField(max_length=10)
    other_symptoms = models.TextField(blank=True, null=True)
    need_work_accommodation = models.CharField(max_length=20)
    need_work_accommodation_other = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    recovery_routine = models.TextField(blank=True, null=True)
    emotional_stability_after_self = models.IntegerField()

    class Meta:
        db_table = 'daily_report_mornings'  # テーブル名をユニークに設定


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10, choices=[('morning', 'Morning'), ('evening', 'Evening')]
    )
    answer_type = models.CharField(max_length=50, default="未指定")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuestionnaireOption(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    option_value = models.IntegerField()

    class Meta:
        db_table = 'questionnaire_options'

    def __str__(self):
        return f'{self.questionnaire.title}: {self.option_text} ({self.option_value})'


class QuestionnaireThreshold(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    threshold_min = models.IntegerField(null=True, blank=True)
    threshold_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questionnaire_thresholds'
        unique_together = ('employee', 'questionnaire')


class DailyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_datetime = models.DateTimeField()
    report_type = models.CharField(
        max_length=10, choices=[('morning', 'Morning'), ('evening', 'Evening')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_reports'
        ordering = ['report_datetime']

    def __str__(self):
        return f"{self.employee.name} - {self.report_type} - {self.report_datetime}"


class DailyReportAnswer(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answer = models.TextField()
    threshold_value = models.IntegerField(null=True, blank=True)  # threshold_value フィールドを追加
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'daily_report_answers'

