from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Survey, SurveyResponse, SurveyException
from .serializers import SurveySerializer, SurveyResponseSerializer

class SurveysListCreate(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyResponseCreate(generics.CreateAPIView):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

    def post(self, request):
        try:
            return super().post(request)
        except SurveyException as e:
            return Response(e.message, status=status.HTTP_403_FORBIDDEN)