import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PDF_SAVE_PATH = os.path.expanduser("~/Desktop")
