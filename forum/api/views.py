from django.views.generic.base import TemplateView
from models import Topic


class LoginPageView(TemplateView):
    template_name = 'main_page.html'


class TopicView(TemplateView):
    template_name = 'topic_page.html'

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context["topic_name"] = Topic.objects.get(id=kwargs['topic_id']).name # Just to show proper title of a topic in a page :)
        return context