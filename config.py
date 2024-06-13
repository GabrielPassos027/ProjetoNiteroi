import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/SICONFI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PDF_SAVE_PATH = os.path.expanduser("~/Desktop")