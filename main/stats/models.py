from django.db import models


class TotalStats(models.Model):
    added = models.DateTimeField(auto_now_add=True)  # todo check if there is some trigger to autoupdate this field
    word_counts = models.TextField()
    top_10_words = models.TextField()


class AuthorStats(models.Model):
    author = models.ForeignKey('scraper.Author', related_name='stats_author', on_delete=models.CASCADE)
    word_counts = models.TextField()
    top_10_words = models.TextField()
