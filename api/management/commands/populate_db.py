from django.core.management import BaseCommand
from api.models import Post, User, Comment, Tag
from django.utils import lorem_ipsum
import random


class Command(BaseCommand):
    help = "Populate a database tables"

    def handle(self, *args, **kwargs):
        user = User.objects.filter(username="admin").first()

        if not user:
            user = User.objects.create_superuser(username="admin", password="secret")

        for name in ["Python", "C++", "JavaScript"]:
            Tag.objects.create(name=name)

        tags = Tag.objects.all()
        for i in range(7):
            selected_tags= random.sample(list(tags), random.randint(1,3))
            post = Post.objects.create(
                    title=lorem_ipsum.paragraph(),
                    description=lorem_ipsum.paragraph(),
                    user=user,
                )
            post.tag.add(*selected_tags)

        posts = Post.objects.all()
        for i in range(5):
            for post in random.sample(list(posts), 1):
                for _ in range(random.randint(1,4)):
                    Comment.objects.create(
                        user=user, post=post, text=lorem_ipsum.paragraph()
                    )
