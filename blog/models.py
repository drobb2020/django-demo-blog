from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


def user_directory_path(instance, filename):
    return "posts/{0}/{1}".format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    excerpt = RichTextField()
    image = models.ImageField(
        upload_to=user_directory_path, default="posts/default.jpg"
    )
    image_caption = models.CharField(max_length=100, default="Photo by Blog")
    slug = models.SlugField(max_length=255, unique_for_date="published_date")
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = RichTextField()
    status = models.CharField(max_length=10, choices=options, default="draft")
    favourites = models.ManyToManyField(
        User, related_name="favourite", default=None, blank=True
    )
    likes = models.ManyToManyField(User, related_name="like", default=None, blank=True)
    like_count = models.BigIntegerField(default="0")
    objects = models.Manager()
    newmanager = NewManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog:post-single", args=[self.slug])

    class Meta:
        ordering = ("-published_date",)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    content = models.TextField(null=True, blank=True)
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["publish"]

    def __str__(self):
        return f"Comment by {self.name}"
