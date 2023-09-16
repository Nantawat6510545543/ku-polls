import datetime

from django.test import TestCase
from django.utils import timezone

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
