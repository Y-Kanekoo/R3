from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('general', 'General')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'

class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    answer_type = models.CharField(max_length=50, default="未指定")  # デフォルト値を指定
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionnaireOption(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)  # 選択肢のテキスト（例：'良い'、'悪い'など）
    option_value = models.IntegerField()  # 選択肢に対応する数値（例：1, 2, 3）

    # class Meta:
    #     db_table = 'questionnaire_options'

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
    report_type = models.CharField(max_length=10, choices=[('morning', 'Morning'), ('evening', 'Evening')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_reports'

class DailyReportAnswer(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    threshold_value = models.FloatField()

    class Meta:
        db_table = 'daily_report_answers'

    def __str__(self):
        return f'{self.questionnaire.title} - Answer: {self.answer}'
