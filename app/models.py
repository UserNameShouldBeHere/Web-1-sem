from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileManager(models.Manager):
    def get_popular_members(self):
        return self.annotate(total=models.Count("post")).order_by("-total")[:5]
    def get_by_user_id(self, user_id):
        return self.filter(user=User.objects.get(id=user_id))[0]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads/avatar/% Y/% m/% d/", blank=True, null=True)

    objects = ProfileManager()

class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.annotate(total=models.Count("post")).order_by("-total")[:5]
    def get_id(self, tag):
        return self.values("id").filter(name=tag)[0]["id"]

class Tag(models.Model):
    name = models.CharField(max_length=24)

    objects = TagManager()

class PostManager(models.Manager):
    def sort_by_date(self):
        return self.order_by("-created_at")
    def sort_by_hot(self):
        return self.order_by("-rating", "-created_at")
    def get_by_id(self, post_id):
        return self.filter(id=post_id)[0]
    def get_by_tag(self, tag):
        return self.filter(tags=Tag.objects.get_id(tag))

class Post(models.Model):
    title = models.TextField()
    text = models.TextField()
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    liked_by = models.ManyToManyField("Profile", blank=True, related_name="post_liked_by")
    disliked_by = models.ManyToManyField("Profile", blank=True, related_name="post_disliked_by")

    objects = PostManager()

class CommentManager(models.Manager):
    def get_by_post(self, post_id):
        return self.filter(post=post_id).order_by('-created_at')

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=0)
    liked_by = models.ManyToManyField("Profile", blank=True, related_name="comment_liked_by")
    disliked_by = models.ManyToManyField("Profile", blank=True, related_name="comment_disliked_by")

    objects = CommentManager()
