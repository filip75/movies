from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the movie")
    year = models.IntegerField(help_text="Years of the movie's premiere")
    director = models.TextField(max_length=500, help_text="Directors of the movie")
    plot = models.TextField(max_length=2000, help_text="Plot of the movie", blank=True)


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, help_text="Content of the comment")
