from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import home, board_topics, new_topic, reply_topic
from ..models import Board, Topic, Post
from ..forms import PostForm

class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django boards')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        Post.objects.create(message='Lorem Ipsum', topic=self.topic, created_by=self.user)

class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super(LoginRequiredReplyTopicTests, self).setUp()
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, "{login_url}?next={url}".format(login_url=login_url,url=self.url))



class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super(ReplyTopicTests, self).setUp()
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_forms(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PostForm)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func,reply_topic)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super(SuccessfulReplyTopicTests, self).setUp()
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(self.url)


    def test_new_topic_valid_post_data(self):
        data = {
            'message':'Lorem Ipsum dolor sit amet'
        }
        response = self.client.post(self.url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
        self.assertEquals(len(Post.objects.all()), 2)

    def test_new_topic_valid_post_redirect(self):
        data = {
            'message':'Lorem Ipsum dolor sit amet'
        }
        url = reverse('topic_posts', kwargs={'pk':self.board.pk, 'topic_pk': self.topic.pk })
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        response = self.client.post(self.url,data)
        self.assertRedirects(response, topic_posts_url)



class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super(InvalidReplyTopicTests, self).setUp()
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.response = self.client.get(self.url)


    def test_reply_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        :return:
        '''
        response = self.client.post(self.url, {})
        form = response.context['form']
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


    def test_reply_topic_invalid_post_data_empty_fields(self):
        data = {
            'message': ''
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
        self.assertEquals(len(Post.objects.all()),1)
