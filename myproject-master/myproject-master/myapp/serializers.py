# myapp/serializers.py
from rest_framework import serializers
from .models import DailyReportMorning

class DailyReportMorningSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReportMorning
        fields = '__all__'  # 全てのフィールドをシリアライズ
