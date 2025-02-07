import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://public_user_account:p5rICIDxj0@localhost/gym')
    SQLALCHEMY_BINDS = {
        'admin': os.getenv('ADMIN_DATABASE_URL', 'postgresql://admin_user:SK23rKv0zf@localhost/gym')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './static/img')