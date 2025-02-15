from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import (
    CommentSerializer, GroupSerializer, PostSerializer
)
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

    def get_post(self, post_id):
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_post(self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post(self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Недостаточно прав для редактирования!')
        return super(CommentViewSet, self).perform_destroy(instance)
