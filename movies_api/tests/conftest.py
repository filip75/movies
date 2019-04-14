from json import dumps
from unittest.mock import patch, Mock

import pytest
from requests.exceptions import ConnectionError

from movies_api.config import config
from movies_api.models import Movie, Comment
from movies_api.utils import URL

SHREK_JSON = {'Title': 'Shrek', 'Year': '2001', 'Rated': 'PG', 'Released': '18 May 2001', 'Runtime': '90 min',
              'Genre': 'Animation, Adventure, Comedy, Family, Fantasy', 'Response': 'True'}
FAIL_JSON = {'Response': 'False'}
WRONG_URL = 'WRONG'


@pytest.fixture
def shrek_movie() -> Movie:
    return Movie(id=1, title='shrek', movie_data=dumps(SHREK_JSON))


@pytest.fixture
def save_shrek(transactional_db, shrek_movie: Movie) -> Movie:
    shrek_movie.save()
    return shrek_movie


@pytest.fixture
def shrek_comment(save_shrek: Movie) -> Comment:
    return Comment(movie=save_shrek, content='shrek comment')


@pytest.fixture
def comment_shrek(shrek_comment: Comment) -> Comment:
    shrek_comment.save()
    return shrek_comment


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
            elif WRONG_URL in url:
                raise ConnectionError
            return not_found_mock

        get_mock.side_effect = side_effect
        yield
