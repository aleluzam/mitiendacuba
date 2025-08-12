import os
from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

def get_mysql_uri():
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'



def get_uri():
    DATABASE_URL = os.getenv("DATABASE_URL")
    return DATABASE_URL

