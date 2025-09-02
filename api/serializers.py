from rest_framework import serializers
from .models import Post, Comment, Tag


class PostSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()

    def get_title(self, obj):
        title = obj.title
        return title[:30] + "..." if len(title) > 30 else ""

    def get_description(self, obj):
        desc = obj.description
        return desc[:60] + "..." if len(desc) > 60 else ""

    def get_total_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "user",
            "tag",
            "total_comments",
        )


class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    def get_comment(self, obj):
        text = obj.text
        return text[:80] + "..." if len(text) > 80 else text

    class Meta:
        model = Comment
        fields = ("user", "comment")


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_title(self, obj):
        title = obj.title
        return title[:30] + "..." if len(title) > 30 else title

    def get_description(self, obj):
        description = obj.description
        return description[:60] + "..." if len(description) > 60 else description

    class Meta:
        model = Post
        fields = ("title", "description", "created_at", "user", "tag", "comments")
