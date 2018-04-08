from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm

# Create your tests here.


class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


    def test_view_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SignUpForm)


class SuccessfulSignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        data ={'username': 'john',
               'email': 'john@mymail.com',
               'password1':'abcdef123456',
               'password2': 'abcdef123456'}
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_athentication(self):
        response = self.client.get(self.home_url)
        user = response.context['user']
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url, data)


    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_donot_create_user(self):
        self.assertFalse(User.objects.exists())