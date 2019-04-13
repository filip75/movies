class Config:
    config_dict = {
        'api_key': 'cd1dc8e7'
    }

    def __getattr__(self, item):
        return self.config_dict.get(item, None)


config = Config()
