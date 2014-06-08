from rest_framework import generics, permissions
from serializers import PostSerializer, TopicSerializer, ForumUserSerializer, SystemUserSerializer
from permissions import AuthorCanEditPermission, IsStaffOrTargetUser
from models import Post, Topic, ForumUser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import viewsets, views
from rest_framework.response import Response
from .auth import BasicForumAuthentication


class AuthView(views.APIView):
    authentication_classes = (BasicForumAuthentication, )
    serializer_class = SystemUserSerializer

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(self.serializer_class(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})


class SystemUserViewSet(viewsets.ModelViewSet):
    serializer_class = SystemUserSerializer
    model = User

    def get_permissions(self):
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser())


class ForumUserList(generics.ListAPIView):
    model = ForumUser
    serializer_class = ForumUserSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class ForumUserDetail(generics.RetrieveAPIView):
    model = ForumUser
    serializer_class = ForumUserSerializer
    lookup_field = 'pk'
    permission_classes = [
        permissions.IsAdminUser
    ]


class PostMixin(object):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        AuthorCanEditPermission
    ]

    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.author = ForumUser.objects.get(system_user__id=self.request.user.id)
        return super(PostMixin, self).pre_save(obj)


class PostList(PostMixin, generics.ListCreateAPIView):
    pass


class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class TopicMixin(object):
    model = Topic
    serializer_class = TopicSerializer
    permission_classes = [
        AuthorCanEditPermission
    ]

    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.author = ForumUser.objects.get(system_user__id=self.request.user.id)
        return super(TopicMixin, self).pre_save(obj)



class TopicList(TopicMixin, generics.ListCreateAPIView):
    pass


class TopicDetail(TopicMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(author__id=self.kwargs.get('pk'))