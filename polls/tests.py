import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
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

    # Test case set 3: can_vote
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


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

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
