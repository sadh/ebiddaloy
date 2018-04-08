from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core import mail

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func, auth_views.password_reset)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class PasswordResetTestCase(TestCase):
    def setUp(self, email):
        User.objects.create_user(username='John', email=email, password='123acbdef')
        self.url = reverse('password_reset')
        self.response = self.client.post(self.url, {'email': email})

class SuccessfulPasswordResetTests(PasswordResetTestCase):
    def setUp(self):
        super(SuccessfulPasswordResetTests, self).setUp('john@doe.com')

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        self.url = reverse('password_reset')
        self.response = self.client.post(self.url, {'email': 'donotexists@email.com'})


    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)


    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func, auth_views.password_reset_done)

class PasswordResetConfirmTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', email='john@doe.com', password='123acbdef')
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk)).decode()
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(self.url, follow=True)

class PasswordResetConfirmTests(PasswordResetConfirmTestCase):
    def setUp(self):
        super(PasswordResetConfirmTests, self).setUp()

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/{uibd64}/{token}/'.format(uibd64=self.uid, token=self.token))
        self.assertEquals(view.func, auth_views.password_reset_confirm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

class InvalidPasswordResetConfirmTests(PasswordResetConfirmTestCase):
    def setUp(self):
        super(InvalidPasswordResetConfirmTests, self).setUp()
        self.user.set_password('abcdef123')
        self.user.save()
        self.url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(self.url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))




class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func, auth_views.password_reset_complete)