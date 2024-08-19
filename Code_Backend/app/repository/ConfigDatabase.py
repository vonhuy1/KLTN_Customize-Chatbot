from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase
Base = DeclarativeBase()
from sqlalchemy.engine import create_engine, URL
from dotenv import load_dotenv
import os
load_dotenv()
MYSQL_USER_NAME=os.getenv('MYSQL_USER_NAME')
MYSQL_PASSWORD=os.getenv('MYSQL_PASSWOR')
MYSQL_PORT=os.getenv('MYSQL_PORT')
MYSQL_DATABASE=os.getenv('MYSQL_DATABASE')
MYSQL_HOST=os.getenv('MYSQL_HOST')
#IF USE DOCKER HOST = host.docker.internal
def get_db_engine():
    dsn = URL.create(
        drivername="mysql+pymysql",
        username=MYSQL_USER_NAME,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE
    )
    connect_args = {}
    return create_engine(
        dsn,
        connect_args=connect_args,
        pool_size=20,
        pool_recycle=300,
        pool_pre_ping=True
    )

def get_db_engine1():
    dsn = URL.create(
        drivername="mysql+pymysql",
        username=MYSQL_USER_NAME,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE
    )
    connect_args = {}
    return create_engine(
        dsn,
        connect_args=connect_args,
        pool_size=20,
        pool_recycle=300,
        pool_pre_ping=True
    )