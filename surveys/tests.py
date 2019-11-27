from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from surveys.models import SurveyResponse, Survey


class SurveyTests(APITestCase):
    def setUp(self):
        Survey.objects.bulk_create([
            Survey(user_id=4, survey_name='First survey', available_places=3),
            Survey(user_id=4, survey_name='Second survey', available_places=2),
            Survey(user_id=10, survey_name='Third survey', available_places=2),
        ])

    def test_list_surveys(self):
        response = self.client.get(path=reverse('surveys'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Survey.objects.count(), 3)

    def test_create_survey(self):
        response = self.client.post(path=reverse('surveys'), data={'user_id': 20, 'survey_name': 'Test Survey', 'available_places': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 4)

    def test_fail_create_survey(self):
        response = self.client.post(path=reverse('surveys'), data={'user_id': 20, 'survey_name': 'Test Survey', 'available_places': -10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Survey.objects.count(), 3)

    def test_create_survey_response(self):
        response = self.client.post(path=reverse('survey-responses'), data={'user_id': 15, 'survey': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyResponse.objects.count(), 1)

    def test_fail_create_survey_response(self):
        response = self.client.post(path=reverse('survey-responses'), data={'user_id': 15, 'survey': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SurveyResponse.objects.count(), 0)

    def test_fail_create_survey_response_places_limit(self):
        s = Survey(user_id=6, survey_name='Full survey', available_places=0) # 4th survey
        s.save()
        response = self.client.post(path=reverse('survey-responses'), data={'user_id': 15, 'survey': 4})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # might be better to use assertraises
        self.assertEqual(SurveyResponse.objects.filter(survey=s).count(), 0)