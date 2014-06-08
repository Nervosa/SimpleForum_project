from django.conf.urls import patterns, include, url

from django.contrib import admin
from api.views import LoginPageView, TopicView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', LoginPageView.as_view(), name='login'),
    url(r'^topics/(?P<topic_id>\d+)$', TopicView.as_view(), name='topic'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('forum.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
