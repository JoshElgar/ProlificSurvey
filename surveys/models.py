from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class SurveyException(Exception):
    def __init__(self, message='Survey related exception occurred'):
        self.message = message

class SurveyPlaceLimitException(SurveyException):
    def __init__(self, message='Survey has no remaining places'):
        self.message = message

class SurveyResponseNoMatchingSurveyException(SurveyException):
    def __init__(self, message='No matching survey was found'):
        self.message = message

class SurveyResponse(models.Model):
    user_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(to='Survey', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # could eventually put check for 1 survey response per user id

        survey_obj = Survey.objects.get(id=self.survey.id)
        # only save if related survey's available_places limit would not be broken
        if survey_obj.available_places > 0:
            survey_obj.available_places = survey_obj.available_places - 1
            survey_obj.save()
            super().save(*args, **kwargs)
        else:
            raise SurveyPlaceLimitException()
        
        return

class Survey(models.Model):
    user_id = models.PositiveIntegerField()
    survey_name = models.CharField(max_length=255)
    available_places = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.id}"


