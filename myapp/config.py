import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_PROTECTION_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 300
    CKEDITOR_PKG_TYPE = 'full'
    FLASK_ADMIN_SWATCH = 'cerulean'