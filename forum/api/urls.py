from django.conf.urls import url, patterns, include

from rest_framework import routers

from .api import PostList, PostDetail, UserPostList
from .api import TopicList, TopicDetail
from .api import ForumUserList, ForumUserDetail
from .api import SystemUserViewSet
from .api import AuthView


router = routers.DefaultRouter()
router.register(r'', SystemUserViewSet, 'systemuser')

user_urls = patterns('',
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/posts$', UserPostList.as_view(), name='userpost-list'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/$', ForumUserDetail.as_view(), name='user-detail'),
    url(r'^/$', ForumUserList.as_view(), name='user-list')
)

auth_urls = patterns('',
    url(r'', AuthView.as_view(), name='authenticate')
)

post_urls = patterns('',
    url(r'^$', PostList.as_view(), name='post-list'),
    url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail')
)

topic_urls = patterns('',
    url(r'^$', TopicList.as_view(), name='topic-list'),
    url(r'^/(?P<pk>\d+)$', TopicDetail.as_view(), name='topic-detail')
)

urlpatterns = patterns('',
    url(r'^users', include(user_urls)),
    url(r'^system_users', include(router.urls)),
    url(r'^posts', include(post_urls)),
    url(r'^topics', include(topic_urls)),
    url(r'^auth/$', include(auth_urls)),
)