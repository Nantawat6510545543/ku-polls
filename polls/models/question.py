import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Represents a question in the application.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published',
                                    default=timezone.now)
    end_date = models.DateTimeField('Date ended',
                                    null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the Question object.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Checks if the question was published recently.

        Returns:
            bool: True if the question was published within the last day,
                  False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Is published?',
    )
    def is_published(self):
        """
        Checks if the question is published.

        Returns:
            bool: True if the current date is on or after the question's
            publication date.
        """
        now = timezone.now()
        return now >= self.pub_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Can vote?',
    )
    def can_vote(self):
        """
        Checks if voting is allowed for this question.

        Returns:
            bool: True if the current date/time
                  is between pub_date and end_date (if not null).
                  If end_date is null,
                  voting is allowed anytime after pub_date.
        """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date
