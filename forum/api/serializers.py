from rest_framework import serializers

from forum.api.models import Post, Topic, ForumUser
from django.contrib.auth.models import User


class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_staff')
        write_only_fields = ('password', )

    def restore_object(self, attrs, instance=None):
        user = super(SystemUserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        user.save()
        return user


class ForumUserSerializer(serializers.ModelSerializer):

    system_user = SystemUserSerializer()
    posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list')

    class Meta:
        model = ForumUser
        fields = ('id', 'system_user', 'avatar', 'posts')


class TopicSerializer(serializers.ModelSerializer):
    post_set = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail')
    author = serializers.RelatedField(many=False)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'author', 'op_post', 'post_set']


class PostSerializer(serializers.ModelSerializer):
    topic = serializers.HyperlinkedRelatedField(many=False, view_name='topic-detail')
    author = serializers.RelatedField(many=False) #ForumUserSerializer()

    def get_validation_exclusions(self):
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['author', 'modified_at', ]

    class Meta:
        model = Post
        # fields = ['topic', 'number_in_topic', 'text', 'author', 'created_at' ]