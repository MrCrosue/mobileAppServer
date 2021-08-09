import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fixtripuser:VZ4TCA3b@web2.nipingp.ru/fixtrip_v2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False