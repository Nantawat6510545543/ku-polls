from django.db import models
from . import Question


class Choice(models.Model):
    """
    Represents a choice for a particular question in the application.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """
        Returns the number of votes for this choice.
        """
        return self.vote_set.count()

    def __str__(self):
        """
        Returns a string representation of the Choice object.
        """
        return self.choice_text
