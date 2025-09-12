from django.urls import path
from .views import post_views, comment_views, tag_views, user_views

urlpatterns = [
    path('posts/', view=post_views.PostListCreateAPIView.as_view(), name='posts'),
    path('posts/<int:post_id>', view=post_views.PostDetailAPIView.as_view(), name='post-details'),
    path('posts/<int:post_id>/comments', view=comment_views.PostCommentsListCreateAPIView.as_view(), name='post-comments'),
    path('posts/<int:post_id>/comments/<int:comment_id>', view=comment_views.PostCommentsDetailAPIView.as_view(), name='post-comment-details'),
    path('user/delete', view=user_views.UserDeleteAPIView.as_view(),name='user-delete'),
    path('tags/', view=tag_views.TagListAPIView.as_view(), name='tags'),
]