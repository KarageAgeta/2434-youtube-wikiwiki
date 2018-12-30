import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class TestConfig(Config):
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class StagingConfig(Config):
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class ProductionConfig(Config):
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    @staticmethod
    def init_app(app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'stage': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
