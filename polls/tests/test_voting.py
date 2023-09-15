import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelVotingTests(TestCase):
    def test_can_vote_when_end_date_is_null(self):
        """
        Testing that can_vote returns True when end_date is null.
        """
        question = Question(question_text="Test question",
                            pub_date=timezone.now())
        self.assertTrue(question.can_vote())

    def test_can_vote_within_voting_period(self):
        """
        Testing that can_vote returns True when within the voting period.
        """
        pub_date = timezone.now() - datetime.timedelta(hours=1)
        end_date = timezone.now() + datetime.timedelta(hours=1)
        question = Question(question_text="Test question", pub_date=pub_date,
                            end_date=end_date)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        Testing that can_vote returns False when before the pub_date.
        """
        pub_date = timezone.now() + datetime.timedelta(hours=1)
        question = Question(question_text="Test question", pub_date=pub_date)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        Testing that can_vote returns False when after the end_date.
        """
        end_date = timezone.now() - datetime.timedelta(hours=1)
        pub_date = timezone.now() - datetime.timedelta(hours=2)
        question = Question(question_text="Test question", pub_date=pub_date,
                            end_date=end_date)
        self.assertFalse(question.can_vote())
