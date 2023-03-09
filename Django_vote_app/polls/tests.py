import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
#Models or Views
class QuestionModelTests(TestCase):

    def setUp(self) -> None:
        self.question = Question(question_text="which game developer company is the best?")


    def test_was_recentrly_published_with_future_questions(self):
        """was_recently_publshed returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_recently_published(), False)


    def test_was_recentrly_published_with_present_questions(self):
        """was_recently_publshed returns True for questions whose pub_date is in the rpesent day"""
        time = timezone.now() - datetime.timedelta(hours=22)
        self.question.pub_date = time
        self.assertIs(self.question.was_recently_published(), True)


    def test_was_recentrly_published_with_past_questions(self):
        """was_recently_publshed returns False for questions whose pub_date is more than a day in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        self.question.pub_date = time
        self.assertIs(self.question.was_recently_published(), False)