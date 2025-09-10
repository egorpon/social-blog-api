from rest_framework.test import APITestCase
from .models import User, Post, Comment, Tag
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class PostAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="test")
        self.user = User.objects.create_user(username="john", password="test")
        self.tag_python = Tag.objects.create(name="Python")
        self.tag_js = Tag.objects.create(name="JavaScript")
        self.admin_post = Post.objects.create(
            title="Test 1", description="test1 test", user=self.admin
        )
        self.user_post = Post.objects.create(
            title="Test 2", description="test2 test2", user=self.user
        )
        self.admin_post.tag.add(self.tag_js)
        self.admin_post.tag.add(self.tag_python)

        self.user_post.tag.add(self.tag_python)
        self.admin_post_comment = Comment.objects.create(
            text="dkaskdaskdaskdsakd", post=self.admin_post, user=self.admin
        )
        self.user_post_comment = Comment.objects.create(
            text="dkaskdaskdaskdsakd", post=self.admin_post, user=self.user
        )

        self.posts = reverse("posts")
        self.admin_post_details = reverse(
            "post-details", kwargs={"post_id": self.admin_post.id}
        )
        self.user_post_details = reverse(
            "post-details", kwargs={"post_id": self.user_post.id}
        )
        self.post_comments = reverse(
            "post-comments", kwargs={"post_id": self.admin_post.id}
        )
        self.post_comments_detail = reverse(
            "post-comment-details",
            kwargs={
                "post_id": self.admin_post.id,
                "comment_id": self.admin_post_comment.id,
            },
        )
        self.tags = reverse("tags")

    def test_user_can_create_post(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "title": "Test 3",
            "description": "test test",
            "tag": [self.tag_js.id, self.tag_python.id],
        }
        response = self.client.post(self.posts, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_all_posts(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.posts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_any_post(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.admin_post_details)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_only_own_post(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.delete(self.user_post_details)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_users_post(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.delete(self.admin_post_details)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_only_own_posts(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "title": "updated title",
            "description": "updated description",
            "tag": [self.tag_js.id],
        }
        response = self.client.put(self.user_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_users_post(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "title": "updated title",
            "description": "updated description",
            "tag": [self.tag_js.id],
        }

        response = self.client.put(self.admin_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_partial_update_other_users_post(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "title": "updated title",
            "description": "updated description",
            "tag": [self.tag_js.id],
        }

        response = self.client.patch(self.admin_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_partial_update_own_posts(self):
        self.client.login(username=self.user.username, password="test")
        data = {"tag": [self.tag_js.id]}

        response = self.client.patch(self.user_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_see_all_post_comments(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.post_comments)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_comments(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "text":'test'
        }
        response = self.client.post(self.post_comments, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)