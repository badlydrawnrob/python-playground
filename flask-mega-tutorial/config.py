# Flask config
DEBUG = True

# WTF FlaskForm
WTF_CSRF_ENABLES = True
SECRET_KEY = 'you-will-never-guess'

# SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Flask-Mail
# MAIL_SERVER = 'smtp.example.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'username'
# MAIL_PASSWORD = 'password'
