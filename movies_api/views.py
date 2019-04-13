from json import dumps
from typing import Optional

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from movies_api.models import Movie, Comment
from movies_api.serializers import MovieSerializer, CommentSerializer
from movies_api.utils import get_movie_data


class MoviesView(APIView):
    @staticmethod
    def get(_: Request, title: Optional[str] = None):
        if title:
            try:
                return Response(MovieSerializer(Movie.objects.get(title=title.strip().lower())).data)
            except Movie.DoesNotExist:
                raise Http404
        return Response(MovieSerializer(Movie.objects.all(), many=True).data)

    @staticmethod
    def post(request: Request):
        title = request.data.get('title', '')
        movie_data = dumps(get_movie_data(title))
        request.data['movie_data'] = movie_data
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentsView(APIView):
    @staticmethod
    def get(_: Request, movie: Optional[int] = None):
        if movie:
            try:
                return Response(CommentSerializer(Comment.objects.filter(movie=movie), many=True).data)
            except Comment.DoesNotExist:
                raise Http404
        return Response(CommentSerializer(Comment.objects.all(), many=True).data)

    @staticmethod
    def post(request: Request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
