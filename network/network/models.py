from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import AutoField, CharField, DateTimeField, FloatField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FileField


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass

class Post(models.Model):
    post_id = AutoField(primary_key=True)
    poster = ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    title = CharField(max_length=200)
    content = CharField(max_length=400)
    upload_date = DateTimeField()
    likes = IntegerField(default=0)

    def __str__(self):
        return f"{self.post_id} | posted by {self.poster} on {self.upload_date} with {self.likes} likes | "

class Follows(models.Model):
    follower = ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"{self.follower} is following {self.followed}"

class Like(models.Model):
    liker = ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    liked_post = ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.liker} liked {self.liked_post}"