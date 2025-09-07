from rest_framework import serializers
from .models import Post, Comment, Tag


class PostListSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    def get_title(self, obj):
        title = obj.title
        return title[:30] + "..." if len(title) > 30 else title

    def get_description(self, obj):
        desc = obj.description
        return desc[:60] + "..." if len(desc) > 60 else desc

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
            "total_comments",
        )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "description", "tag")


class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source="text")

    class Meta:
        model = Comment
        fields = ("id", "user", "datetime", "comment")


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text",)


class PostDetailSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    total_comments = serializers.SerializerMethodField()

    def get_total_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = (
            "title",
            "description",
            "user",
            "created_at",
            "tag",
            "image",
            "total_comments",
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "title",
            "description",
            "tag",
            "image",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug")
