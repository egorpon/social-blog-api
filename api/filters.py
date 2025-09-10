import django_filters
from .models import Post, Comment


class MultiTagFilter(django_filters.BaseCSVFilter, django_filters.CharFilter):
    def filter(self, qs, value):
        tags = value or []
        if not tags:
            return qs
        for tag in tags:
            qs = qs.filter(tag__slug = tag)
        return qs

class PostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name="created_at__date")
    tag  = MultiTagFilter(field_name = 'tag')

    class Meta:
        model = Post
        fields = {
            "created_at": ["exact", "lt", "gt", "range"],
            "user": ["exact"],
            'tag':['exact']
        }


class CommentFilter(django_filters.FilterSet):
    datetime = django_filters.DateFilter(field_name="datetime__date")

    class Meta:
        model = Comment
        fields = {"user": ["exact"], "datetime": ["exact", "lt", "gt", "range"]}
