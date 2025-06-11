import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///pulke.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

