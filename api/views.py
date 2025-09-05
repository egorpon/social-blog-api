from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Tag, Comment
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer, PostUpdateSerializer,TagSerializer, CommentSerializer, CommentCreateUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import isAdminOrOwner
# Create your views here.

################ POSTS ##################
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.prefetch_related("tag", "comments")
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        self.serializer_class = PostListSerializer
        if self.request.method == 'POST':
            self.serializer_class = PostCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = "post_id"
    permission_classes = [isAdminOrOwner]

    def get_serializer_class(self):
        self.serializer_class = PostDetailSerializer
        if self.request.method in ["PUT", "PATCH"]:
            self.serializer_class = PostUpdateSerializer
        return super().get_serializer_class()    
    

################ COMMENTS ##################
class PostCommentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        self.serializer_class = CommentSerializer
        if self.request.method == "POST":
            self.serializer_class = CommentCreateUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        post = self.kwargs.get("post_id")
        return qs.filter(post__id=post)

class PostCommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [isAdminOrOwner]
    lookup_url_kwarg = 'comment_id'

    def get_serializer_class(self):
        self.serializer_class = CommentSerializer
        if self.request.method in ["PUT","PATCH"]:
            self.serializer_class = CommentCreateUpdateSerializer
        return super().get_serializer_class()


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagPostsListAPIView(generics.ListAPIView):
    queryset = Post.objects.prefetch_related("tag", "comments")
    serializer_class = PostListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        qs = super().get_queryset()
        return qs.filter(tag__slug=slug)
