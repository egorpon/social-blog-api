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
        self.post_user_comments_detail = reverse(
            "post-comment-details",
            kwargs={
                "post_id": self.admin_post.id,
                "comment_id": self.user_post_comment.id,
            },
        )
        self.post_admin_comments_detail = reverse(
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
            "title": "New Post",
            "description": "new post new post",
            "tag": [self.tag_python.id, self.tag_js.id],
        }
        response = self.client.post(self.posts, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["tag"], [self.tag_python.id, self.tag_js.id])

        post = Post.objects.get(id=response.data["id"])
        self.assertIsNotNone(post.created_at)
        self.assertEqual(post.user, self.user)

    def test_user_can_view_all_posts(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.posts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Post.objects.count())

    def test_user_can_filter_posts_by_tags(self):
        self.client.login(username=self.user.username, password="test")

        response = self.client.get(self.posts + "?tag=python,javascript")
        self.assertEqual(
            len(response.data),
            Post.objects.filter(tag__slug="python")
            .filter(tag__slug="javascript")
            .count(),
        )

        response = self.client.get(self.posts + "?tag=python")
        self.assertEqual(
            len(response.data), Post.objects.filter(tag__slug="python").count()
        )

    def test_user_can_retrieve_any_post(self):
        self.client.login(username=self.user.username, password="test")

        response = self.client.get(self.admin_post_details)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.admin_post.title)

        response = self.client.get(self.user_post_details)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.user_post.title)

    def test_user_can_delete_only_own_post(self):
        self.client.login(username=self.user.username, password="test")

        response = self.client.delete(self.user_post_details)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(self.admin_post_details)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_only_his_own_posts(self):
        self.client.login(username=self.user.username, password="test")

        data = {
            "title": "updated title",
            "description": "updated description",
            "tag": [self.tag_js.id],
        }

        response = self.client.put(self.user_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data["title"])

        post = Post.objects.filter(title=data['title']).first()
        self.assertEqual(response.data['tag'], list(post.tag.values_list('id', flat=True)))

        response = self.client.put(self.admin_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_partial_update_only_own_posts(self):
        self.client.login(username=self.user.username, password="test")
        data = {
            "tag": [self.tag_js.id],
        }
        response = self.client.patch(self.user_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tag'], data['tag'])

        post = Post.objects.filter(id=self.user_post.id).first()
        self.assertEqual(response.data['tag'], list(post.tag.values_list('id', flat=True)))

        response = self.client.patch(self.admin_post_details, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_view_all_post_comments(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.post_comments)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), Comment.objects.filter(post=self.admin_post.id).count()
        )

    def test_user_can_create_comments(self):
        self.client.login(username=self.user.username, password="test")
        data = {"text": "test"}
        response = self.client.post(self.post_comments, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["text"], data["text"])
        comment = Comment.objects.get(id=response.data["id"])
        self.assertIsNotNone(comment.datetime)
        self.assertEqual(comment.user, self.user)

    def test_user_can_update_and_partial_update_his_own_comments(self):
        self.client.login(username=self.user.username, password="test")
        data = {"text": "test"}

        response = self.client.put(self.post_user_comments_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["text"], data["text"])
        comment = Comment.objects.get(id=response.data["id"])
        self.assertEqual(response.data['text'], comment.text)

        response = self.client.patch(self.post_admin_comments_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_his_own_comments(self):
        self.client.login(username=self.user.username, password="test")

        response = self.client.delete(self.post_user_comments_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(self.post_admin_comments_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
