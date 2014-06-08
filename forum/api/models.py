from django.db import models
from django.contrib.auth.models import User
import datetime


class ForumUser(models.Model):
    system_user = models.OneToOneField(User, null=False)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __unicode__(self):
        return self.system_user.username

class Topic(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(ForumUser)
    op_post = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, default=datetime.datetime.today())
    modified_at = models.DateTimeField(blank=True, default=datetime.datetime.today())

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.modified_at = datetime.datetime.today()
        return super(Topic, self).save(*args, **kwargs)


class Post(models.Model):
    topic = models.ForeignKey(Topic, blank=False, null=False)
    number_in_topic = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, default=datetime.datetime.today())
    modified_at = models.DateTimeField(blank=True, default=datetime.datetime.today())
    author = models.ForeignKey(ForumUser)
    image = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True)

    def __unicode__(self):
        return "Post #" + str(self.number_in_topic) + " in topic " + self.topic.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.modified_at = datetime.datetime.today()
        self.number_in_topic = Post.objects.filter(topic_id=self.topic_id).count() + 1
        return super(Post, self).save(*args, **kwargs)