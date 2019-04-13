from unittest.mock import patch

import pytest

from movies_api.config import config
from movies_api.tests.conftest import SHREK_JSON
from movies_api.utils import get_movie_data, URL


class TestUtils:
    @pytest.mark.usefixtures('omdbapi')
    def test_get_movie_data(self):
        fetched_data = get_movie_data('Shrek')

        assert SHREK_JSON == fetched_data

    @pytest.mark.usefixtures('omdbapi')
    def test_get_movie_data_fail(self):
        fetched_data = get_movie_data('Shrek 2')

        assert None is fetched_data

    @patch('requests.get')
    def test_get_movie_data_white_spaces_upper(self, get_mock):
        get_movie_data('    ShRek    ')

        get_mock.assert_called_with(URL.format('shrek', config.api_key))
