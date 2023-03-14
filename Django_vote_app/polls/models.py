import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
#not neded to define id, Django creates it automatically
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('published date')

    def __str__(self) -> str:
        return self.question_text
    
    def was_recently_published(self):
        return timezone.now() >=self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text