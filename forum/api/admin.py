from django.contrib import admin

from forum.api.models import Topic, Post, ForumUser

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(ForumUser)