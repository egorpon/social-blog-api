from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Post, Tag, Comment
from ..serializers import (
    CommentSerializer,
    CommentCreateUpdateSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ..permissions import isAdminOrOwner
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import CommentFilter
from rest_framework import filters
# Create your views here.


class PostCommentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CommentFilter
    search_fields = ["text"]
    ordering_fields = ["datetime"]

    def get_serializer_class(self):
        self.serializer_class = CommentSerializer
        if self.request.method == "POST":
            self.serializer_class = CommentCreateUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        post = self.kwargs.get("post_id")
        return qs.filter(post__id=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return serializer.save(user=self.request.user, post=post)


class PostCommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [isAdminOrOwner]
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        if post_id:
            qs = qs.filter(post__id = post_id)
        return qs

    def get_serializer_class(self):
        self.serializer_class = CommentSerializer
        if self.request.method in ["PUT", "PATCH"]:
            self.serializer_class = CommentCreateUpdateSerializer
        return super().get_serializer_class()
