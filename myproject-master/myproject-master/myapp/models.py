# myapp/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_type = models.CharField(
        max_length=10, choices=[('admin', 'Admin'), ('general', 'General')])
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
    THRESHOLD_TYPE_CHOICES = [
        ('min', 'Minimum Value'),
        ('max', 'Maximum Value'),
        ('exact', 'Exact Value')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # 従業員
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE)  # 質問
    min_value = models.FloatField(null=True, blank=True)  # 最小しきい値
    max_value = models.FloatField(null=True, blank=True)  # 最大しきい値
    exact_value = models.FloatField(null=True, blank=True)  # 特定のしきい値
    threshold_type = models.CharField(
        max_length=10, choices=THRESHOLD_TYPE_CHOICES)  # しきい値のタイプ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'thresholds'  # テーブル名を指定
        # 同じ従業員と質問に対して重複するしきい値を防ぐ
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'questionnaire'], name='unique_employee_questionnaire')
        ]

    def clean(self):
        # しきい値タイプに基づいて、適切なしきい値が設定されているかをチェック

        # しきい値タイプが 'min' の場合、min_value が設定されていないとエラー
        if self.threshold_type == 'min' and self.min_value is None:
            raise ValidationError('最小しきい値が設定されていません。')

        # しきい値タイプが 'max' の場合、max_value が設定されていないとエラー
        if self.threshold_type == 'max' and self.max_value is None:
            raise ValidationError('最大しきい値が設定されていません。')

        # しきい値タイプが 'exact' の場合、exact_value が設定されていないとエラー
        if self.threshold_type == 'exact' and self.exact_value is None:
            raise ValidationError('特定のしきい値が設定されていません。')

    def __str__(self):
        return f"{self.employee.name} - {self.questionnaire.title} - {self.threshold_type}"


class Notification(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE)  # 通知の対象者（従業員）
    message = models.TextField()  # 通知メッセージ
    created_at = models.DateTimeField(auto_now_add=True)  # 通知が作成された日時
    is_read = models.BooleanField(default=False)  # 既読かどうかのフラグ

    class Meta:
        db_table = 'notifications'  # テーブル名を指定
        ordering = ['-created_at']  # 通知が新しい順に並べる

    def __str__(self):
        return f"Notification for {self.employee.name}: {self.message}"


def send_notification(questionnaire, message):
    # 通知メッセージを作成
    administrators = Employee.objects.filter(
        employee_type='admin')  # 管理者のみフィルタ

    # すべての管理者に対して通知を送信
    for admin in administrators:
        Notification.objects.create(
            employee=admin,
            message=f"アンケート {questionnaire.title}: {message}"
        )
