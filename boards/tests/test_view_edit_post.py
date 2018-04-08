from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import PostUpdateView
from ..models import Board, Topic, Post


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django boards')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='Lorem Ipsum', topic=self.topic, created_by=self.user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super(PostUpdateViewTests, self).setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)


    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/posts/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super(LoginRequiredPostUpdateViewTests, self).setUp()

    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, "{login_url}?next={url}".format(login_url=login_url, url=self.url))


class UnAuthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super(UnAuthorizedPostUpdateViewTests, self).setUp()
        username = 'jane'
        password = '123'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)
