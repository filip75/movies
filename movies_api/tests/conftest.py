from unittest.mock import patch, Mock

import pytest

from movies_api.config import config
from movies_api.models import Movie, Comment
from movies_api.utils import URL

SHREK_JSON = {'Title': 'Shrek', 'Year': '2001', 'Rated': 'PG', 'Released': '18 May 2001', 'Runtime': '90 min',
              'Genre': 'Animation, Adventure, Comedy, Family, Fantasy', 'Response': 'True'}
FAIL_JSON = {'Response': 'False'}


@pytest.fixture
def save_shrek(transactional_db) -> Movie:
    movie = Movie(id=1, title='shrek', movie_data='')
    movie.save()
    return movie


@pytest.fixture
def comment_shrek(save_shrek: Movie):
    comment = Comment(movie=save_shrek, content='')
    comment.save()


@pytest.fixture
def omdbapi():
    with patch('requests.get') as get_mock:
        shrek_request = patch('requests.Request')
        shrek_request.json = Mock(return_value=SHREK_JSON)
        not_found_mock = patch('requests.Request')
        not_found_mock.json = Mock(return_value=FAIL_JSON)

        def side_effect(url: str):
            if url == URL.format('shrek', config.api_key):
                return shrek_request
            return not_found_mock

        get_mock.side_effect = side_effect
        yield
