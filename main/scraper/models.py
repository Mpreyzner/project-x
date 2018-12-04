from django.db import models


class Post(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=False)
    # author = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey('Author', related_name='post_author', on_delete=models.CASCADE)
    content = models.TextField()
    language = models.CharField(max_length=2, blank=False)


class Author(models.Model):
    name = models.CharField(max_length=255, blank=False)
    tokenized_name = models.CharField(max_length=255, blank=False)
