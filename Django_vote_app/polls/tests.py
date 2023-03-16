import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.
#Models or Views
def create_question(text, days):
    '''
    Create a question with the given "question_text", and will be published 
    the given number of days offset to now (negative days for questions in the past, and positive days for questions that have yet to be published) 
    '''
    time = (timezone.now() + datetime.timedelta(days=days))
    return Question.objects.create(question_text=text, pub_date=time)


def create_choice(pk, choice_text, votes=0):
    """
    Create a choice that have the pk(primary key is a number) of a specific question
    with the given "choice_text" and with the given "votes"(votes starts in zero)
    """
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)



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


class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        '''
        If doesnt exist a question, display an apropiate message
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Polls not found!')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_no_future_question_published(self):
        '''
        If there's exist a question yet to be published (timedate in the future), then don't display it
        '''
        create_question("future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Polls not found!')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_display_past_question(self):
        '''
        For question with pub_date in the past, to be dysplayed in our index page
        '''
        question = create_question("past question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_create_both_questions_type_display_only_past(self):
        '''
        Even if a past question and a future question exist, only display 
        the past one on index page
        '''
        past_question = create_question("past question", -30)
        future_question = create_question("future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])


    def test_create_two_past_question_display_both(self):
        '''
        for two past questions created, display both on index page
        '''
        past_question1 = create_question("past question 1", -30)
        past_question2 = create_question("past question 2", -40)
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question1, past_question2])


    def test_create_two_future_question_display_both(self):
        '''
        for two future questions created, display none of them on index page
        '''
        future_question1 = create_question("future question", 30)
        future_question2 = create_question("future question", 40)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_question_without_choices(self):
        """
        Quetions have no choices aren't displayed in the index view
        """
        question = create_question("Cuál es tu curso favorito?", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])



    def test_question_with_choices(self):
        """
        Question with choices are displayed in the index view
        """
        question = create_question("Cuál es tu curso favorito?", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="Curso Básico de Django", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Curso de Introducción a la Nube con Azure", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The deatail view of a question with a pub_date in te future
        return a "404 error not found".
        """
        future_question = create_question("future question", 30)
        url = reverse("polls:detail", args=(future_question.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays question's text
        """
        past_question = create_question("past question", -30)
        url = reverse("polls:detail", args=(past_question.pk, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        


class ResultViewTest(TestCase):

    def test_with_past_question(self):
        """
        The result view with a pub date in the past display the 
        question's text
        """
        past_question = create_question("past question", days=-15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)



class ResultViewTest(TestCase):

    def test_with_past_question(self):
        """
        The result view with a pub date in the past display the 
        question's text
        """
        past_question = create_question("past question", -15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_with_future_question(self):
        """
        Questions with a future date aren't displayed and this return a 404 error(not found) 
        until the date is the specified date
        """
        future_question = create_question("this is a future question", 30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)