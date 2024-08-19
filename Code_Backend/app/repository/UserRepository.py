from sqlalchemy.orm import sessionmaker
from models import Database_Entity
from repository import ConfigDatabase as cf
import pytz , datetime
from datetime import timedelta
user = Database_Entity.User

def getUserIdByAccessToken(token:str) -> int:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.access_token == token).one_or_none()
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.access_token == token).one_or_none()
        session.close()
        return user_record

def getUserIdByAccessTokenAndUserId(token:str,user_id: int) -> int:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.access_token == token,user.id == user_id).one_or_none()
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.access_token == token,user.id == user_id).one_or_none()
        session.close()
        return user_record

def getUserByEmail(email: str) -> user:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user).filter(user.email == email).one_or_none()
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user).filter(user.email == email).one_or_none()
        session.close()
        return user_record

def getUserIdByEmail(email: str) -> user.id:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.email == email).one_or_none()[0]
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.email == email).one_or_none()[0]
        session.close()
        return user_record

def getUserById(user_id: str) -> user:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user).filter(user.id == user_id).one_or_none()
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user).filter(user.id == user_id).one_or_none()
        session.close()
        return user_record

def getRefreshTokenUserByAccessToken(token: str) -> user.refresh_token:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.refresh_token).filter(user.access_token == token).one_or_none()
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.refresh_token).filter(user.access_token == token).one_or_none()
        session.close()
        return user_record


def getUserIdByRefreshToken(refreshToken: str) -> user.refresh_token:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.refresh_token == refreshToken).one_or_none()[0]
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.id).filter(user.refresh_token == refreshToken).one_or_none()[0]
        session.close()
        return user_record

def getRefreshTokenUserById(user_id: str) -> user.refresh_token:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.refresh_token).filter(user.id == user_id).one_or_none()[0]
        session.close()
        return user_record
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_record = session.query(user.refresh_token).filter(user.id == user_id).one_or_none()[0]
        session.close()
        return user_record

def getEmailUser(email:str) -> user.email:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.email == email).one_or_none()
        session.close()
        return user_email
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.email == email).one_or_none()
        session.close()
        return user_email

def getEmailUserById(user_id:int) -> user.email:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.id == user_id).one_or_none()[0]
        session.close()
        return user_email
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.id == user_id).one_or_none()[0]
        session.close()
        return user_email

def getEmailUserByIdFix(user_id:int) -> user.email:
  try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.id == user_id).one_or_none()
        session.close()
        return user_email
  except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.id == user_id).one_or_none()
        session.close()
        return user_email



def getEmailUserByAccessToken(token: str) -> user.email:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.access_token == token).one_or_none()
        session.close()
        return user_email
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_email = session.query(user.email).filter(user.access_token == token).one_or_none()
        session.close()
        return user_email


def addUser(email: str, access_token: str, refresh_token: str, expires_at: datetime.datetime) -> None:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_user = Database_Entity.User(
            email=email,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        session.add(new_user)
        session.commit()
        session.close()
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_user = Database_Entity.User(
            email=email,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        session.add(new_user)
        session.commit()
        session.close()


def updateUserLogin(email: str, access_token: str, refresh_token: str, expires_at: datetime.datetime) -> bool:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.email == email).one_or_none()
        if user_update:
            user_update.email = email
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.email == email).one_or_none()
        if user_update:
            user_update.email = email
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

       
def updateAccessToken(user_id: int,access_token: str, expires_at: datetime.datetime) -> None:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == user_id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.expires_at = expires_at
            session.commit()
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == user_id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.expires_at = expires_at
            session.commit()

def updateAccessTokenById(id: int,access_token: str, expires_at: datetime.datetime) -> None:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()


def UpdateAccessTokenRefreshToken(email: str, access_token: str, refresh_token: str, expires_at: datetime.datetime) -> None:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.email == email).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.email == email).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()

def UpdateAccessTokenRefreshTokenById(user_id: int,access_token: str, refresh_token: str, expires_at: datetime.datetime) -> None:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == user_id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()
 except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        user_update = session.query(user).filter(user.id == user_id).one_or_none()
        if user_update:
            user_update.access_token = access_token
            user_update.refresh_token = refresh_token
            user_update.expires_at = expires_at
            session.commit()
        session.close()