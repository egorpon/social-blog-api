from django.urls import path
from . import views

urlpatterns = [
    path('posts/', view=views.PostListAPIView.as_view(), name='posts'),
    path('posts/<int:post_id>', view=views.PostDetailAPIView.as_view(), name='post'),
    path('posts/<int:post_id>/comments', view=views.PostCommentsListAPIView.as_view(), name='post-comments'),
    path('tags/', view=views.TagListAPIView.as_view(), name='tags'),
    path('tags/<slug:slug>/posts', view=views.TagPostsListAPIView.as_view(), name='tag-posts')
]