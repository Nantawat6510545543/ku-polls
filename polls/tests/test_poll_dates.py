import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionModelPollTests(TestCase):
    # Test case set 1:was_published_recently
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    # Test case set 2: is_published
    def test_is_published_with_future_pub_date(self):
        """
        is_published() should return False for a question
        with a future pub_date.
        """
        future_time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_default_pub_date(self):
        """
        is_published() should return True for a question
        with the default pub_date (now).
        """
        now = timezone.now()
        default_pub_question = Question(pub_date=now)
        self.assertIs(default_pub_question.is_published(), True)

    def test_is_published_with_past_pub_date(self):
        """
        is_published() should return True for a question
        with a pub_date in the past.
        """
        past_time = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=past_time)
        self.assertIs(past_question.is_published(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        should return a 302 redirect to the index page.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('polls:index'))

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
