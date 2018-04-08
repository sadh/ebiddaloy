"""ebiddaloy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from boards import views as boards_views
from administrator import views as admin_views

urlpatterns = [
    url(r'^$', boards_views.home, name='home'),
    url(r'^signup/$',accounts_views.signup,name='signup'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^login/$',auth_views.login,
        {'template_name':'login.html'},name='login'),
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(),
        {'template_name': 'my_account.html'}, name='my_account'),
    url(r'^settings/password/$', auth_views.password_change,
        {'template_name': 'password_change.html'}, name='password_change'),
    url(r'^settings/password/done/$', auth_views.password_change_done,
        {'template_name': 'password_change_done.html'}, name='password_change_done'),
    url(r'^reset/$', auth_views.password_reset,
         {'template_name':'password_reset.html',
         'email_template_name':'password_reset_email.html',
          'subject_template_name': 'password_reset_subject.txt',}, name='password_reset'),
    url(r'^reset/done/$', auth_views.password_reset_done,
        {'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.password_reset_complete,
        {'template_name':'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^schooladmin/$', admin_views.AdminDashBoardView.as_view(), name='admin_dashboard'),
    url(r'^boards/(?P<pk>\d+)/$',boards_views.TopicListView.as_view(),name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', boards_views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', boards_views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        boards_views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^admin/', admin.site.urls),
]
