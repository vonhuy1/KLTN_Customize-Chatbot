from sqlalchemy.orm import sessionmaker
from models import Database_Entity
from repository import ConfigDatabase as cf
user_info = Database_Entity.UserInfo
users = Database_Entity.User
from sqlalchemy.orm import sessionmaker
import sys
import os

def getUserInfo(user_id: int) -> user_info:
 try:
   email = session.query(users.email).filter(users.id == user_id).one_or_none()
   if email:
        email = email[0]
        user_record= session.query(user_info).filter(user_info.email == email).one_or_none()
        if user_record:
         session.close()
         return user_record
        else:
         session.close()
         return None
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == user_id).one_or_none()
    if email:
        email = email[0]
        user_record= session.query(user_info).filter(user_info.email == email).one_or_none()
        if user_record:
         session.close()
         return user_record
        else:
         session.close()
         return None

def getUserInfoByEmail(email:str) -> user_info:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    user_record= session.query(user_info).filter(user_info.email == email).one_or_none()
    if user_record:
        session.close()
        return user_record
    else:
        session.close()
        return None
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    user_record= session.query(user_info).filter(user_info.email == email).one_or_none()
    if user_record:
        session.close()
        return user_record
    else:
        session.close()
        return None



def addUserInfo(uid: str, email: str, display_name: str, photo_url: str) -> None:
 try:
     engine = cf.get_db_engine()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        new_user = user_info(
           uid = uid,
           email = email,
           display_name = display_name,
           photo_url = photo_url
        )
        session.add(new_user)
        session.commit()
        session.close()
 except:
     engine = cf.get_db_engine1()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        new_user = user_info(
           uid = uid,
           email = email,
           display_name = display_name,
           photo_url = photo_url
        )
        session.add(new_user)
        session.commit()
        session.close()

def updateUserInfo(user_id, uid: str, email: str, display_name: str, photo_url: str) -> None:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        email = session.query(users.email).filter(users.id == user_id).one_or_none()
        user_update= session.query(user_info).filter(user_info.email == email).one_or_none()
        if user_update is not None:
            user_update.uid = uid,
            user_update.display_name = display_name,
            user_update.photo_url = photo_url
            session.commit()
        session.close()
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        email = session.query(users.email).filter(users.id == user_id).one_or_none()
        user_update= session.query(user_info).filter(user_info.email == email).one_or_none()
        if user_update is not None:
            user_update.uid = uid,
            user_update.display_name = display_name,
            user_update.photo_url = photo_url
            session.commit()
        session.close()


def updateImage(user_id, photo_url: str) -> None:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        email = session.query(users.email).filter(users.id == user_id).one_or_none()
        user_update= session.query(user_info).filter(user_info.email == email).one_or_none()
        if user_update is not None:
            user_update.photo_url = photo_url
            session.commit()
        session.close()
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
       email = session.query(users.email).filter(users.id == user_id).one_or_none()
       user_update = session.query(user_info).filter(user_info.email == email).one_or_none()
       if user_update is not None:
           user_update.photo_url = photo_url
           session.commit()
       session.close()

