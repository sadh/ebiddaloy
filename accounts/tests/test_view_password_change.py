from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'john'
        password = 'secret123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        url = reverse('password_change')
        self.client.login(username=username,password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/settings/password/')
        self.assertEquals(view.func, auth_views.password_change)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginrequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response,r'{login_url}?next={url}'.format(login_url=login_url,url=url))

class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data=data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super(SuccessfulPasswordChangeTests, self).setUp(
            {
                'old_password':'old_password',
                'new_password1': 'new_password',
                'new_password2': 'new_password'
            }
        )

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))


    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context['user']
        self.assertTrue(user.is_authenticated)



class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super(InvalidPasswordChangeTests, self).setUp(data={})
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))