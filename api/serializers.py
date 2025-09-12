from rest_framework import serializers
from .models import Post, Comment, Tag, User


class PostSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    total_comments = serializers.SerializerMethodField()

    def get_total_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "user",
            "created_at",
            "tag",
            "image",
            "total_comments",
        )


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ("id","title", "description", "tag", "image")


class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source="text")
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "user", "datetime", "comment")

    def get_user(self, obj):
        if obj.user is None:
            return None
        return obj.user.id


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ("id","text",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug")

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()