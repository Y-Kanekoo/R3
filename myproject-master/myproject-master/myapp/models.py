from django.db import models

# Create your models here.

# myapp/models.py

class DailyReportMorning(models.Model):
    name = models.CharField(max_length=255)
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    sleep_quality = models.CharFField(max_length = 150)
    had_dinner_yesterday = models.CharField(max_length = 10)
    had_breakfast_today = models.CharField(max_length = 10)
    medicine_time = models.CharField(max_length = 10)
    current_condition = models.CharField(max_length = 10)
    current_condition_other = models.TextField(blank=True, null=True)
    anxiety_level = models.CharField(max_length = 10)
    current_emotion = models.CharField(max_length = 10)
    communication_willingness = models.CharField(max_length = 10)
    physical_condition = models.CharField(max_length = 10)
    concentration_level = models.CharField(max_length = 10)
    physical_discomfort = models.CharField(max_length = 10)
    self_esteem = models.CharField(max_length = 10)
    willingness_to_depend = models.CharField(max_length = 10)
    feeling_needed = models.CharField(max_length = 10)
    other_symptoms = models.TextField(blank=True, null=True)
    need_work_accommodation = models.CharField(max_length = 20)
    need_work_accommodation_other = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    recovery_routine = models.TextField(blank=True, null=True)
    emotional_stability_after_self = models.IntegerField()


    class Meta:
        db_table = 'Daily_report_morning'  # テーブル名を指定

        
    def __str__(self):
        return self.name
