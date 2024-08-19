from sqlalchemy.orm import sessionmaker
import sys
import os
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, app_path)
from models import Database_Entity
from repository import ConfigDatabase as cf
chat_history = Database_Entity.ChatHistory
users = Database_Entity.User
detail_chat = Database_Entity.DetailChat
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import sys
import os

def getIdChatHistoryByUserIdAndNameChat(user_id:int,name_old :str) -> chat_history.id:
  try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
    chat_id = session.query(chat_history.id).filter(chat_history.email == email, chat_history.name_chat == name_old).scalar()
    session.commit()
    if chat_id:
        session.close()
        return chat_id
    else:
        session.close()
        return None
  except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
    chat_id = session.query(chat_history.id).filter(chat_history.email == email, chat_history.name_chat == name_old).scalar()
    session.commit()
    if chat_id:
        session.close()
        return chat_id
    else:
        session.close()
        return None

def getIdChatHistoryByUserIdAndNameChatNew(user_id:int,name_old :str) -> chat_history.id:
  try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
    chat_id = session.query(chat_history.id).filter(chat_history.email == email, chat_history.name_chat == name_old).scalar()
    session.commit()
    if chat_id:
        session.close()
        return chat_id
    else:
        session.close()
        return None
  except:
      engine = cf.get_db_engine1()
      Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
      with Session() as session:
          email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
          chat_id = session.query(chat_history.id).filter(chat_history.email == email,
                                                          chat_history.name_chat == name_old).scalar()
          session.commit()
          if chat_id:
              session.close()
              return chat_id
          else:
              session.close()
              return None

def updateNameChatHistory(user_id: int,name_old :str,name_new:str) -> bool:
 try:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    try:
      email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
      session.query(chat_history).filter(chat_history.email == email,chat_history.name_chat == name_old).update({chat_history.name_chat: name_new})
      session.commit()
      session.close()
      return True
    except:
       session.rollback()
       session.close()
       return False
 except:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    try:
      email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
      session.query(chat_history).filter(chat_history.email == email,chat_history.name_chat == name_old).update({chat_history.name_chat: name_new})
      session.commit()
      session.close()
      return True
    except:
       session.rollback()
       session.close()
       return False

def deleteChatHistory(user_id,chat_name: str) -> bool:
 try:
  try:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
    session.query(chat_history).filter(chat_history.email == email, chat_history.name_chat == chat_name).delete()
    session.commit()
    session.close()
    return True
  except Exception as e:
        session.rollback()
        session.close()
        return False
 except:
   try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
     email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
     session.query(chat_history).filter(chat_history.email == email, chat_history.name_chat == chat_name).delete()
     session.commit()
     session.close()
     return True
   except Exception as e:
        session.rollback()
        session.close()
        return False


def getChatHistoryByEmail(email: str) -> chat_history:
   try:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
       chat_history1 = session.query(chat_history).filter(chat_history.email == email)
       if chat_history1:
          session.commit()
          session.close()
          return chat_history1
       session.close()
       return None
   except:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
       chat_history1 = session.query(chat_history).filter(chat_history.email == email)
       if chat_history1:
          session.commit()
          session.close()
          return chat_history1
       session.close()
       return None

from sqlalchemy.orm import aliased

def delete_last_chat_detail_by_chat_name_and_email(chat_name: str, user_id: int) -> bool:
    try:
        engine = cf.get_db_engine()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            email = session.query(users.email).filter(users.id == user_id).one_or_none()
            if not email:
                return False
            email = email[0]
            last_chat_detail = (session.query(detail_chat)
                                .join(chat_history, detail_chat.chat_id == chat_history.id)
                                .filter(chat_history.name_chat == chat_name, chat_history.email == email)
                                .order_by(detail_chat.id.desc())
                                .first())

            if last_chat_detail:
                session.delete(last_chat_detail)
                session.commit()
                return True
            return False
    except:
        engine = cf.get_db_engine1()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            email = session.query(users.email).filter(users.id == user_id).one_or_none()
            if not email:
                return False
            email = email[0]
            last_chat_detail = (session.query(detail_chat)
                                .join(chat_history, detail_chat.chat_id == chat_history.id)
                                .filter(chat_history.name_chat == chat_name, chat_history.email == email)
                                .order_by(detail_chat.id.desc())
                                .first())

            if last_chat_detail:
                session.delete(last_chat_detail)
                session.commit()
                return True
            return False
def getChatHistoryByChatIdAndUserId(chat_id: int, user_id: int) -> chat_history:
    try:
        engine = cf.get_db_engine()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
            chat_history1 = session.query(chat_history).filter(chat_history.id == chat_id,chat_history.email == email).one_or_none()
            if chat_history1:
                session.commit()
                session.close()
                return True
            session.close()
            return None
    except:
        engine = cf.get_db_engine1()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            email = session.query(users.email).filter(users.id == id).one_or_none()[0]
            chat_history1 = session.query(chat_history).filter(chat_history.email == email)
            if chat_history1:
                session.commit()
                session.close()
                return True
            session.close()
            return None


def getChatHistoryById(id: int) -> chat_history:
   try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
       email = session.query(users.email).filter(users.id == id).one_or_none()[0]
       chat_history1 = session.query(chat_history).filter(chat_history.email == email)
       if chat_history1:
          session.commit()
          session.close()
          return chat_history1
       session.close()
       return None
   except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
       email = session.query(users.email).filter(users.id == id).one_or_none()[0]
       chat_history1 = session.query(chat_history).filter(chat_history.email == email)
       if chat_history1:
          session.commit()
          session.close()
          return chat_history1
       session.close()
       return None

def addChatHistory(user_id: str, name_chat:str)->None:
 try:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
        new_user = chat_history(
           email = email,
           name_chat = name_chat
        )
        session.add(new_user)
        session.commit()
        session.close()
 except:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
        email = session.query(users.email).filter(users.id == user_id).one_or_none()[0]
        new_user = chat_history(
           email = email,
           name_chat = name_chat
        )
        session.add(new_user)
        session.commit()
        session.close()