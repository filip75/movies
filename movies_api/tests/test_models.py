import pytest
from django.db.utils import IntegrityError

from movies_api.models import Movie, Comment


@pytest.mark.usefixtures('transactional_db')
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


class TestComment:
    def test_create_comment(self, save_shrek):
        comment = Comment(movie=save_shrek, content='')
        count = Comment.objects.count()

        comment.save()

        assert Comment.objects.count() > count

    @pytest.mark.usefixtures('transactional_db')
    def test_create_comment_wrong_movie(self):
        movie = Movie(id=11, title='Shrek', movie_data='')
        comment = Comment(movie=movie, content='')

        with pytest.raises(IntegrityError):
            comment.save()
