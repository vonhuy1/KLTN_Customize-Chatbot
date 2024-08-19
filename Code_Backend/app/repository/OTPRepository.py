from sqlalchemy.orm import sessionmaker
from models import Database_Entity
from repository import ConfigDatabase as cf
otp_user = Database_Entity.OTP
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import sys
import os

def getOtpByEmail(email: str) -> otp_user:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    user_record= session.query(otp_user).filter(otp_user.email == email).one_or_none()
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
    user_record= session.query(otp_user).filter(otp_user.email == email).one_or_none()
    if user_record:
        session.close()
        return user_record
    else:
        session.close()
        return None
    
def addOTP(email: str, otp: str) -> None:
    try:
     engine = cf.get_db_engine()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        otp_record = session.query(otp_user).filter_by(email=email).first()
        if otp_record:
            session.delete(otp_record)
            session.commit()
        new_user = otp_user(
           email = email,
           otp= otp 
        )
        session.add(new_user)
        session.commit()
        session.close()
    except:
     engine = cf.get_db_engine1()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        otp_record = session.query(otp_user).filter_by(email=email).first()
        if otp_record:
            session.delete(otp_record)
            session.commit()
        new_user = otp_user(
           email = email,
           otp= otp 
        )
        session.add(new_user)
        session.commit()
        session.close()
       
def deleteOTP(email: str, otp:str) -> None:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
       otp_record = session.query(otp_user).filter_by(email=email, otp=otp).first()
       if otp_record:
            session.delete(otp_record)
            session.commit()
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
       otp_record = session.query(otp_user).filter_by(email=email, otp=otp).first()
       if otp_record:
            session.delete(otp_record)
            session.commit()