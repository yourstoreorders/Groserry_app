import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string hello world'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'product_images')


    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')     
    MAIL_DEFAULT_SENDER = ('MyStore','MyStore@Anvayagrocery.com')

    GROCERY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = 'Grocery Store'
    ORDER_MAIL_RECEIVER = os.environ.get('ORDER_MAIL_RECEIVER')
    WTF_CSRF_TIME_LIMIT = None
    
    STORE_NAME = "My Shop Bucket"
    # FLASKY_ADMIN = os.environ.get('GROCERY_APP_ADMIN')
    
    @staticmethod
    def init_app(app):
      import logging
      from logging.handlers import SysLogHandler
      syslog_handler = SysLogHandler()
      syslog_handler.setLevel(logging.WARNING)
      app.logger.addHandler(syslog_handler)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')



class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
  'sqlite:///' + os.path.join(basedir, 'data.sqlite')



config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig
}