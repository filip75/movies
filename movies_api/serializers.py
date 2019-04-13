from rest_framework import serializers

from movies_api.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'movie_data')


class CommentSerializer:
    class Meta:
        model = Comment
        fields = ('movie', 'content')
