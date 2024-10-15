# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DailyReportMorning
from .serializers import DailyReportMorningSerializer

class DailyReportMorningList(APIView):
    def get(self, request):
        reports = DailyReportMorning.objects.all()
        serializer = DailyReportMorningSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DailyReportMorningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
