import os


class Config:
    # app
    APP_NAME = 'Handy Calculator'
    APPLICATION_ROOT = '/handy-calc'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    ACCEPTED_FILE_TYPES = ['.jpeg', '.jpg', '.png']
    MAX_CONTENT_LENGTH = 240 * 1024 * 1024
    # mathpix
    MATHPIX_API = 'https://api.mathpix.com/v3/text'
    MATHPIX_APP_ID = os.environ.get('MATHPIX_APP_ID')
    MATHPIX_APP_KEY = os.environ.get('MATHPIX_APP_KEY')
    MATHPIX_CONFIDENCE_THRESHOLD = 0.8

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = 'http://127.0.0.1:5000'


class ProductionConfig(Config):
    DEBUG = False
    HOST = os.environ.get('PRODUCTION_HOST')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}