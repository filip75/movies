from datetime import datetime
from json import dumps
from typing import Optional

from django.db.models import Count
from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from movies_api.models import Movie, Comment
from movies_api.serializers import MovieSerializer, CommentSerializer
from movies_api.utils import get_movie_data

TOTAL_COMMENTS = 'total_comments'
RANK = 'rank'


class MoviesView(APIView):
    @staticmethod
    def get(_: Request, movie: Optional[int] = None):
        if movie:
            try:
                return Response(MovieSerializer(Movie.objects.get(id=movie)).data)
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
        request.data.pop('date', None)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TopView(APIView):
    @staticmethod
    def get(request: Request):
        start_date = request.GET.get('start_date', None)
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        end_date = request.GET.get('end_date', None)
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        ranking = Comment.objects
        if start_date and end_date:
            ranking = ranking.filter(date__range=(start_date, end_date))
        elif start_date:
            ranking = ranking.filter(date__gte=start_date)
        elif end_date:
            ranking = ranking.filter(date__lte=end_date)
        ranking = ranking. \
            values('movie__id'). \
            annotate(total_comments=Count('movie')). \
            order_by(f'-{TOTAL_COMMENTS}')

        rank = 1
        if len(ranking) > 0:
            ranking[0][RANK] = rank
        for idx in range(1, len(ranking)):
            if ranking[idx][TOTAL_COMMENTS] < ranking[idx - 1][TOTAL_COMMENTS]:
                rank += 1
            ranking[idx][RANK] = rank

        return Response(ranking)
