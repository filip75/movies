import os


class Config:
    config_dict = {
        'api_key': os.environ.get('MOVIES_APIKEY')
    }

    def __getattr__(self, item):
        return self.config_dict.get(item, None)


config = Config()
