import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///fileshare.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}
    AES_KEY = os.getenv('AES_KEY', 'ThisIsASecretKey123').encode('utf-8')
    AES_IV = os.getenv('AES_IV', 'ThisIsAnIV45678').encode('utf-8')