from sqlalchemy.orm import sessionmaker
from models import Database_Entity
from repository import ConfigDatabase as cf
user_login = Database_Entity.UserLogin
users = Database_Entity.User

def getUserLogin(email: str) -> user_login:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    user_record = session.query(user_login).filter(user_login.user_email == email).one_or_none()
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
    user_record = session.query(user_login).filter(user_login.user_email == email).one_or_none()
    if user_record:
        session.close()
        return user_record
    else:
        session.close()
        return None


def getUserLoginById(id: int) -> user_login:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == id).one_or_none()[0]
    user_record = session.query(user_login).filter(user_login.user_email == email).one_or_none()
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
    email = session.query(users.email).filter(users.id == id).one_or_none()[0]
    user_record = session.query(user_login).filter(user_login.user_email == email).one_or_none()
    if user_record:
        session.close()
        return user_record
    else:
        session.close()
        return None
   
def addUserLogin(user_email: str, session_id : str) -> None:
 try:
     engine = cf.get_db_engine()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        new_user = user_login(
           user_email = user_email,
           user_session_id = session_id
        )
        session.add(new_user)
        session.commit()
        session.close()
 except:
     engine = cf.get_db_engine1()
     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     with Session() as session:
        new_user = user_login(
           user_email = user_email,
           user_session_id = session_id
        )
        session.add(new_user)
        session.commit()
        session.close()


def updateUserLogin(email: str, session_id : str ) -> None:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        user_update= session.query(user_login).filter(user_login.user_email == email).one_or_none()
        if user_update is not None:
            user_update.user_session_id = session_id
            session.commit()
        session.close()
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        user_update= session.query(user_login).filter(user_login.user_email == email).one_or_none()
        if user_update is not None:
            user_update.user_session_id = session_id
            session.commit()
        session.close()



def getUserSessionIdByUserEmail(id: int) -> user_login:
 try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
     email = session.query(users.email).filter(users.id == id).one_or_none()[0]
     session.commit()
     user_record= session.query(user_login.user_session_id).filter(user_login.user_email == email).one_or_none()[0]
     session.commit()
     print(user_record)
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
     email = session.query(users.email).filter(users.id == id).one_or_none()[0]
     session.commit()
     user_record= session.query(user_login.user_session_id).filter(user_login.user_email == email).one_or_none()[0]
     session.commit()
     print(user_record)
     if user_record:
        session.close()
        return user_record
     else:
        session.close()
        return None