from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Post
from api.serializers import (
    PostSerializer,
    PostCreateUpdateSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from api.permissions import isAdminOrOwner
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import PostFilter
from rest_framework import filters
# Create your views here.


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.prefetch_related("tag", "comments")
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilter
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        self.serializer_class = PostSerializer
        if self.request.method == "POST":
            self.serializer_class = PostCreateUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = "post_id"
    permission_classes = [isAdminOrOwner]

    def get_serializer_class(self):
        self.serializer_class = PostSerializer
        if self.request.method in ["PUT", "PATCH"]:
            self.serializer_class = PostCreateUpdateSerializer
        return super().get_serializer_class()
