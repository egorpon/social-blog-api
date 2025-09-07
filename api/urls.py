from django.urls import path
from . import views

urlpatterns = [
    path('posts/', view=views.PostListCreateAPIView.as_view(), name='posts'),
    path('posts/<int:post_id>', view=views.PostDetailAPIView.as_view(), name='post'),
    path('posts/<int:post_id>/comments', view=views.PostCommentsListCreateAPIView.as_view(), name='post-comments'),
    path('posts/<int:post_id>/comments/<int:comment_id>', view=views.PostCommentsDetailAPIView.as_view(), name='post-comments-detail'),
    path('tags/', view=views.TagListAPIView.as_view(), name='tags'),
]