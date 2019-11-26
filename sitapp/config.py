import os 
basedir = os.path.abspath(os.path.dirname(__file__)) 

class Config: 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  
    MAIL_SERVER = 'smtp.googlemail.com' # Hostname or IP address of the email server
    MAIL_PORT = 587 # Port of the email server
    MAIL_USE_TLS = True # Enable Transport Layer Security (TLS) security
    MAIL_USE_SSL = False # Enable Secure Sockets Layer (SSL) security
    MAIL_USERNAME = '21400488@handong.edu' #Mail account username
    MAIL_PASSWORD = 'cgifuyedoxfmrgmu' # Mail account password

    MAIL_SUBJECT_PREFIX = 'SIT32006'
    MAIL_SENDER = 'trial'

    @staticmethod 
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True 

class TestingConfig(Config): 
     TESTING = True 

class ProductionConfig(Config): pass

config = { 
    'development': DevelopmentConfig, 
    'testing': TestingConfig, 
    'production': ProductionConfig, 
    'default': DevelopmentConfig 
} 
