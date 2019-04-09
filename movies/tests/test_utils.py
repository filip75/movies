from unittest.mock import patch

from movies.config import config
from movies.utils import get_movie_data, URL

SHREK_JSON = {'Title': 'Shrek', 'Year': '2001', 'Rated': 'PG', 'Released': '18 May 2001', 'Runtime': '90 min',
              'Genre': 'Animation, Adventure, Comedy, Family, Fantasy', 'Response': 'True'}
FAIL_JSON = {'Response': 'False'}


class TestUtils:
    @patch('requests.Request')
    @patch('requests.get')
    def test_get_movie_data(self, get_mock, request_mock):
        request_mock.json.return_value = SHREK_JSON
        get_mock.return_value = request_mock

        fetched_data = get_movie_data('Shrek')

        assert SHREK_JSON == fetched_data

    @patch('requests.Request')
    @patch('requests.get')
    def test_get_movie_data_fail(self, get_mock, request_mock):
        request_mock.json.return_value = FAIL_JSON
        get_mock.return_value = request_mock

        fetched_data = get_movie_data('Shrek')

        assert None is fetched_data

    @patch('requests.get')
    def test_get_movie_data_white_spaces_upper(self, get_mock):
        get_movie_data('    ShRek    ')

        get_mock.assert_called_with(URL.format('shrek', config.api_key))
