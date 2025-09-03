from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Tag, Comment
from .serializers import PostSerializer, PostDetailSerializer, TagSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
# Create your views here.


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.prefetch_related("tag", "comments")
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_url_kwarg = "post_id"


class PostCommentsListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer    
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        qs = super().get_queryset()
        post = self.kwargs.get("post_id")
        return qs.filter(post__id=post)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagPostsListAPIView(generics.ListAPIView):
    queryset = Post.objects.prefetch_related("tag", "comments")
    serializer_class = PostSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        qs = super().get_queryset()
        return qs.filter(tag__slug=slug)
