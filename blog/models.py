from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# sanzhar
class User(AbstractUser):
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    class Meta:
        indexes = [
            models.Index(fields=['author'])
            # tag will be indexed by ManyToMany, given no through kwarg
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['post', 'created_date'])]

    def __str__(self):
        return self.content


@receiver(post_save, sender=Comment)  # caching `complicated` query
def clear_comments_count_cache(sender, instance, **kwargs):
    cache.delete(f'comments_count_{instance.post.id}')
