import pytest
from django.db import IntegrityError

from movies_api.models import Movie


@pytest.mark.django_db
class TestMovie:

    def test_create_movie(self):
        movie = Movie(title='Shrek', movie_data='')
        count = Movie.objects.count()

        movie.save()

        assert Movie.objects.count() > count

    @pytest.mark.usefixtures('save_shrek')
    def test_create_movie_unique(self):
        movie = Movie(title='shrek', movie_data='')

        with pytest.raises(IntegrityError):
            movie.save()
