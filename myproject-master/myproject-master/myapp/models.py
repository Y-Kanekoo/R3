# myapp/models.py
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('general', 'General')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'  # テーブル名を指定

# myapp/models.py
# myapp/models.py
class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    answer_type = models.CharField(max_length=50, default="未指定")  # デフォルト値を指定
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class QuestionnaireOption(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    option_value = models.IntegerField()

    def __str__(self):
        return self.option_text


class QuestionnaireThreshold(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    threshold_min = models.IntegerField(null=True, blank=True)  # 閾値の最小値
    threshold_max = models.IntegerField(null=True, blank=True)  # 閾値の最大値
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questionnaire_thresholds'  # テーブル名を指定
        unique_together = ('employee', 'questionnaire')  # 同じ従業員とアンケートに対する重複を防ぐ

class DailyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    report_datetime = models.DateTimeField()
    report_type = models.CharField(max_length=10, choices=[('morning', 'Morning'), ('evening', 'Evening')])
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
    threshold_value = models.FloatField()  # 閾値フィールドを追加

    class Meta:
        db_table = 'daily_report_answers'  # テーブル名を指定
