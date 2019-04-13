from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True, help_text="Title of the movie")
    movie_data = models.TextField(blank=False)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, help_text="Content of the comment")
