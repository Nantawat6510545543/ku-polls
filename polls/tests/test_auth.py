"""Tests of authentication."""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # to "login" a user using code
from polls.models import Question, Choice
from mysite import settings


class UserAuthTest(django.test.TestCase):
    """
    Tests user authentication.
    """

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "FatChance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Tester"
        self.user1.save()
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_logout(self):
        """A user can log out using the logout url.

        As an authenticated user,
        when I visit /accounts/logout/
        then I am logged out
        and then redirected to the login page.
        """
        logout_url = reverse("logout")
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(logout_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can log in using the login view."""
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {"username": "testuser",
                     "password": "FatChance!"
                     }
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Authentication is required to submit a vote.

        As an unauthenticated user,
        when I submit a vote for a question,
        then I am redirected to the login page,
        or I receive a 403 response (FORBIDDEN)
        """
        vote_url = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote_url, form_data)
        self.assertEqual(response.status_code, 302)
        login_with_next = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_with_next)

    def test_login_with_nonexistent_username(self):
        """
        Make sure a user cannot log in using a username that doesn't exist.
        """
        login_url = reverse("login")
        form_data = {"username": "nonexistent", "password": "RandomPassword!"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")

    def test_login_with_invalid_password(self):
        """
        Make sure a user cannot log in with an invalid password.
        """
        login_url = reverse("login")
        form_data = {"username": self.username, "password": "InvalidPassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")
