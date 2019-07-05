import os.path
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "senha-segura"

FLASK_ADMIN = 'admin@gmail.com'
