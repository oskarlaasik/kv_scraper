import os

postgres_user = os.environ['POSTGRES_USER']
postgres_pwd = os.environ['POSTGRES_PASSWORD']
postgres_db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'
test_db_port = '5433'
SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (postgres_user, postgres_pwd, host, port, postgres_db)

class Config:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (postgres_user, postgres_pwd, host, port, postgres_db)

class TestingConfig(Config):
    TEST_SQLALCHEMY_DATABASE_URI = "sqlite://"

