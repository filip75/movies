import pytest
from rest_framework.test import APIClient


class TestMoviesView:
    @pytest.mark.usefixtures('save_shrek')
    def test_get(self):
        client = APIClient()

        response = client.get('/movies/')

        assert 200 == response.status_code

    @pytest.mark.usefixtures('save_shrek')
    def test_get_title(self):
        client = APIClient()

        response = client.get('/movies/shrek')

        assert 200 == response.status_code

    @pytest.mark.usefixtures('transactional_db', 'omdbapi')
    def test_post(self):
        client = APIClient()

        response = client.post('/movies/', {'title': 'shrek'}, format='json')

        assert 201 == response.status_code

    @pytest.mark.usefixtures('save_shrek', 'omdbapi')
    def test_post_exists(self):
        client = APIClient()

        response = client.post('/movies/', {'title': 'shrek'}, format='json')

        assert 400 == response.status_code


class TestCommentsView:
    @pytest.mark.usefixtures('transactional_db')
    def test_get(self):
        client = APIClient()

        response = client.get('/comments/')

        assert 200 == response.status_code

    @pytest.mark.usefixtures('comment_shrek')
    def test_get_movie(self):
        client = APIClient()

        response = client.get('/comments/movies/1')

        assert 200 == response.status_code

    @pytest.mark.usefixtures('save_shrek')
    def test_post(self):
        client = APIClient()

        response = client.post('/comments/', {'movie': 1, 'content': '123'}, format='json')

        assert 201 == response.status_code

    @pytest.mark.django_db
    def test_post_wrong_movie(self):
        client = APIClient()

        response = client.post('/comments/', {'movie': 1, 'content': '123'}, format='json')

        assert 400 == response.status_code
