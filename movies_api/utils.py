from typing import Optional

import requests

from movies_api.config import config

URL = 'http://www.omdbapi.com/?t={}&apikey={}'


def get_movie_data(title: str) -> Optional[dict]:
    url = URL.format(title.lower().strip(), config.api_key)
    movie_json = requests.get(url).json()
    success = movie_json.get('Response', 'False')
    if success == 'True':
        return movie_json
    return None
