
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.contrib.auth.models import User
from io import BytesIO


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    cover_image = models.ImageField(
        upload_to="post_covers/",
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    content = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Create slug automatically
        if not self.slug:
            self.slug = slugify(self.title)

        # Save post
        super().save(*args, **kwargs)

        # Resize cover image if necessary
        if self.cover_image:
            try:
                with Image.open(self.cover_image.path) as img:
                    img.thumbnail((800, 800))
                    img.save(self.cover_image.path)
            except (OSError, ValueError):
                # Keep the post even if image processing fails
                pass

    def __str__(self):
        return self.title
