import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
#Models or Views
class QuestionModelTests(TestCase):

    def test_was_recentrly_published_with_future_questions(self):
        """was_recently_publshed returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="which game developer company is the best?", pub_date=time)
        self.assertIs(future_question.was_recently_published(), False)