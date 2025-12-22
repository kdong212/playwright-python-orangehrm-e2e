import configparser
import os

class ConfigReader:
    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        config.read(path)
        return config

    @staticmethod
    def get_base_url():
        return ConfigReader.get_config().get('env', 'base_url')