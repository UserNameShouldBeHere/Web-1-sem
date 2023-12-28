from django.core.management import BaseCommand
from faker import Faker
from random import randint
import time

from app.models import Post, Comment, Tag, User, Profile

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        users_count = ratio
        tags_count = ratio
        posts_count = ratio * 10
        comments_count = ratio * 100

        batch = 10000

        User.objects.bulk_create([User(
            username=fake.user_name() + str(randint(1, 100)) + str(randint(1, 100)),
            email=fake.user_name() + '@mail.ru'
            ) for _ in range(ratio)], batch_size=batch)
        print("users filled")

        Profile.objects.bulk_create([Profile(user_id=_ + 1) for _ in range(ratio)], batch_size=batch)
        print("profiles filled")

        Tag.objects.bulk_create([Tag(name=" ".join(fake.catch_phrase()[:16].split("/"))) for _ in range(ratio)], batch_size=batch)
        print("tags filled")

        Post.objects.bulk_create([Post(
            title=fake.job(),
            text=fake.paragraph(nb_sentences=5),
            author=Profile.objects.get(id=fake.random_int(min=0, max=users_count - 1) + 1),
            rating=fake.random_int(min=0, max=40)
        ) for _ in range(posts_count)], batch_size=batch)
        print("posts filled")

        Comment.objects.bulk_create([Comment(
            text=fake.text(max_nb_chars=100),
            post=Post.objects.get(id=fake.random_int(min=0, max=posts_count - 1) + 1),
            author=Profile.objects.get(id=fake.random_int(min=0, max=users_count - 1) + 1),
            rating=fake.random_int(min=0, max=10)
        ) for _ in range(comments_count)], batch_size=batch)
        print("comments filled")

        liked_data = []
        tags_data = []
        for post in Post.objects.all():
            tags = []
            for _ in range(randint(1, 3)):
                new_tag = fake.random_int(min=0, max=tags_count - 1) + 1
                while (post.id, new_tag) in tags:
                    new_tag = fake.random_int(min=0, max=tags_count - 1) + 1
                tags.append((post.id, new_tag))
            tags_data += tags

            liked_by = []
            for _ in range(post.rating):
                new_liked_user = fake.random_int(min=0, max=users_count - 1) + 1
                while (post.id, new_liked_user) in liked_by:
                    new_liked_user = fake.random_int(min=0, max=users_count - 1) + 1
                liked_by.append((post.id, new_liked_user))
            liked_data += liked_by

        Post.tags.through.objects.bulk_create([Post.tags.through(post_id=post_id, tag_id=tag_id) for post_id, tag_id in tags_data], batch_size=batch)
        print("post_tags filled")

        Post.liked_by.through.objects.bulk_create([Post.liked_by.through(post_id=post_id, profile_id=profile_id) for post_id, profile_id in liked_data], batch_size=batch)
        print("post_liked_by filled")

        liked_data = []
        for comment in Comment.objects.all():
            liked_by = []
            for _ in range(comment.rating):
                new_liked_user = fake.random_int(min=0, max=users_count - 1) + 1
                while (comment.id, new_liked_user) in liked_by:
                    new_liked_user = fake.random_int(min=0, max=users_count - 1) + 1
                liked_by.append((comment.id, new_liked_user))
            liked_data += liked_by
        
        Comment.liked_by.through.objects.bulk_create([Comment.liked_by.through(comment_id=comment_id, profile_id=profile_id) for comment_id, profile_id in liked_data], batch_size=batch)
        print("comment_liked_by filled")