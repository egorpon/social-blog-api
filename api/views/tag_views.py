from rest_framework.decorators import api_view
from ..models import Tag
from ..serializers import (
    TagSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from ..permissions import isAdminOrOwner
# Create your views here.


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
