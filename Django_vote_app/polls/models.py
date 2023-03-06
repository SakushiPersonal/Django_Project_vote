from django.db import models

# Create your models here.

class Question(models.Model):
#not neded to define id, Django creates it automatically
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('published date')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)