# myapp/models.py
from django.db import models

class DailyReportMorning(models.Model):
    # 必要なフィールドを定義
    name = models.CharField(max_length=255)
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    sleep_quality = models.IntegerField()
    had_dinner_yesterday = models.IntegerField()
    had_breakfast_today = models.IntegerField()
    medicine_time = models.IntegerField()
    current_condition = models.IntegerField()
    current_condition_other = models.TextField()
    anxiety_level = models.IntegerField()
    current_emotion = models.IntegerField()
    communication_willingness = models.IntegerField()
    physical_condition = models.IntegerField()
    concentration_level = models.IntegerField()
    physical_discomfort = models.IntegerField()
    self_esteem = models.IntegerField()
    willingness_to_depend = models.IntegerField()
    feeling_needed = models.IntegerField()
    other_symptoms = models.TextField()
    need_work_accommodation = models.IntegerField()
    need_work_accommodation_other = models.TextField()
    message = models.TextField()
    recovery_routine = models.TextField()
    emotional_stability_after_self = models.IntegerField()

    class Meta:
        db_table = 'Daily_report_morning'  # テーブル名を指定
