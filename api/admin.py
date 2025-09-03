from django.contrib import admin
from api.models import Comment, Post, User

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(User)