# myapp/views.py
from rest_framework import generics
from .models import DailyReportMorning
from .serializers import DailyReportMorningSerializer

class DailyReportMorningList(generics.ListAPIView):
    queryset = DailyReportMorning.objects.all()
    serializer_class = DailyReportMorningSerializer
