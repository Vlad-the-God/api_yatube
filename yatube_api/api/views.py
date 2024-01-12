from django.core.exceptions import PermissionDenied
from rest_framework import viewsets

from api.serializers import (
    CommentSerializer, GroupSerializer, PostSerializer
)
from api.utils import get_post
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_post(self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_post(self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(CommentViewSet, self).perform_destroy(instance)
