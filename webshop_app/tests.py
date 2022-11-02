from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestUser(TestCase):
    """ Tests registration & login. """

    def test_registration(self):
        """ Checks if the user can register. """
        User.objects.create_user(
            username='test_user',
            password='12345',
        )
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_login(self):
        """ Checks if the user can log in. """
        user = User.objects.create(username='test_user')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='test_user', password='12345')
        self.assertTrue(logged_in)


class TestLoggedView(TestCase):
    """ Tests view available only for logged users. """

    def setUp(self):
        """ Data for further tests. """
        self.client = Client()
        self.logged_url = reverse('logged')

    def test_not_logged_user(self):
        """ Not logged user gets redirect to log in form. """
        response = self.client.get(self.logged_url)
        self.assertRedirects(response, '/login/?next=/logged/')

    def test_logged_user(self):
        """ Logged user enters view. """
        user = User.objects.create_user('test_user', 'test_password')
        self.client.force_login(user=user)
        response = self.client.get(reverse('logged'))
        self.assertEqual(response.status_code, 200)
