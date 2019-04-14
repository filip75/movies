from typing import Optional

import requests
from requests.exceptions import ConnectionError

from movies_api.config import config

URL = 'http://www.omdbapi.com/?t={}&apikey={}'


class FetchMovieDataError(Exception):
    pass


def get_movie_data(title: str) -> Optional[dict]:
    url = URL.format(title.lower().strip(), config.api_key)
    try:
        movie_json = requests.get(url).json()
    except ConnectionError:
        raise FetchMovieDataError
    success = movie_json.get('Response', 'False')
    if success == 'True':
        return movie_json
    return None
