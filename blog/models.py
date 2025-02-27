from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


# creating model manager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# data model for the blog posts
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        null=False,
        blank=False,
    )
    body = CKEditor5Field("Body", config_name="default")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the comment.

        The format is "Comment by <username> on <post title>", where <username> is the username
        of the user who made the comment and <post title> is the title of the post the comment
        is associated with.
        """

        return f"Comment by {self.user} on {self.post.title}"
