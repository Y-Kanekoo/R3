# myapp/models.py
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_type = models.CharField(
        max_length=10, choices=[('admin', 'Admin'), ('general', 'General')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'  # テーブル名を指定


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=[(
        'morning', 'Morning'), ('evening', 'Evening')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questionnaires'  # テーブル名を指定


class DailyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_datetime = models.DateTimeField()
    report_type = models.CharField(max_length=10, choices=[
                                   ('morning', 'Morning'), ('evening', 'Evening')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_reports'  # テーブル名を指定


class DailyReportAnswer(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_report_answers'  # テーブル名を指定


class Threshold(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE)  # 閾値を設定する従業員
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE)  # アンケート項目
    min_value = models.FloatField(null=True, blank=True)  # 最小値
    max_value = models.FloatField(null=True, blank=True)  # 最大値
    exact_value = models.FloatField(null=True, blank=True)  # 特定の値
    threshold_type = models.CharField(max_length=20, choices=[(
        'min', 'Minimum'), ('max', 'Maximum'), ('exact', 'Exact')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'thresholds'
        unique_together = ('employee', 'questionnaire')  # 同じ従業員とアンケートに対する重複を防ぐ
