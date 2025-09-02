from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(["GET"])
def post_list(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


