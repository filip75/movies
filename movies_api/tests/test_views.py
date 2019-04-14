from datetime import datetime

import pytest
from rest_framework.test import APIClient

from movies_api.models import Movie, Comment
from movies_api.serializers import MovieSerializer, CommentSerializer


@pytest.fixture
def api():
    return APIClient()


class TestMoviesView:
    def test_get(self, api: APIClient, save_shrek: Movie):
        response = api.get('/movies/')

        assert response.status_code == 200
        assert response.data == MovieSerializer([save_shrek], many=True).data

    def test_get_id(self, api: APIClient, save_shrek: Movie):
        response = api.get('/movies/1')

        assert response.status_code == 200
        assert response.data == MovieSerializer(save_shrek).data

    @pytest.mark.usefixtures('transactional_db', 'omdbapi')
    def test_post(self, api: APIClient, shrek_movie: Movie):
        response = api.post('/movies/', {'title': 'shrek'}, format='json')

        assert response.status_code == 201
        response.data.pop('id')
        expected_data = MovieSerializer(shrek_movie).data
        expected_data.pop('id')
        assert response.data == expected_data

    @pytest.mark.usefixtures('save_shrek', 'omdbapi')
    def test_post_exists(self, api: APIClient):
        response = api.post('/movies/', {'title': 'shrek'}, format='json')

        assert response.status_code == 400


class TestCommentsView:
    @pytest.mark.usefixtures('transactional_db')
    def test_get(self, api: APIClient, comment_shrek: Comment):
        response = api.get('/comments/')

        assert response.status_code == 200
        assert response.data == CommentSerializer([comment_shrek], many=True).data

    def test_get_movie(self, api: APIClient, comment_shrek: Comment):
        response = api.get('/comments/movies/1')

        assert response.status_code == 200
        assert response.data == CommentSerializer([comment_shrek], many=True).data

    @pytest.mark.usefixtures('save_shrek')
    def test_post(self, api: APIClient, shrek_comment: Comment):
        response = api.post('/comments/', {'movie': shrek_comment.movie.id, 'content': shrek_comment.content},
                            format='json')

        assert response.status_code == 201
        response.data.pop('id')
        shrek_comment.date = datetime.now().strftime("%Y-%m-%d")
        expected_data = CommentSerializer(shrek_comment).data
        expected_data.pop('id')
        assert response.data == expected_data

    @pytest.mark.django_db
    def test_post_wrong_movie(self, api: APIClient):
        response = api.post('/comments/', {'movie': 1, 'content': '123'}, format='json')

        assert response.status_code == 400


@pytest.mark.django_db
class TestTopView:
    def test_get(self, api: APIClient):
        response = api.get('/top/')

        assert response.status_code == 200

    def test_get_start(self, api: APIClient):
        response = api.get('/top/?start_date=2018-01-01')

        assert response.status_code == 200

    def test_get_end(self, api: APIClient):
        response = api.get('/top/?end_date=2018-01-01')

        assert response.status_code == 200

    def test_get_start_end(self, api: APIClient):
        response = api.get('/top/?start_date=2018-01-01&end_date=2018-01-02')

        assert response.status_code == 200

    def test_get_wrong_date_format(self, api: APIClient):
        response = api.get('/top/?start_date=01-01-2018')

        assert response.status_code == 400
