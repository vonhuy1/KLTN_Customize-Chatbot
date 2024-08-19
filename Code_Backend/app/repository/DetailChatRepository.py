from sqlalchemy.orm import sessionmaker
from models import Database_Entity
from repository import ConfigDatabase as cf
detail_chat = Database_Entity.DetailChat
chat_history = Database_Entity.ChatHistory

def getListDetailChatByChatId(chat_id: int) -> detail_chat:
  try:
   engine = cf.get_db_engine1()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    chat_record= session.query(detail_chat).filter(detail_chat.chat_id == chat_id)
    session.commit()
    if chat_record:
        session.close()
        return chat_record
    else:
        session.close()
        return None
  except:
   engine = cf.get_db_engine()
   Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   with Session() as session:
    chat_record= session.query(detail_chat).filter(detail_chat.chat_id == chat_id)
    session.commit()
    if chat_record:
        session.close()
        return chat_record
    else:
        session.close()
        return None

def addDetailChat(chat_id: int, YouMessage: str, AiMessage: str, data_relevant: str, source_file: str) -> None:
  try:
    engine = cf.get_db_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        new_user = detail_chat(
          chat_id = chat_id,
          YouMessage = YouMessage,
          AiMessage = AiMessage,
          data_relevant = data_relevant,
          source_file  = source_file
        )
        session.add(new_user)
        session.commit()
        return new_user.id
        session.close()
  except:
    engine = cf.get_db_engine1()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as session:
        new_user = detail_chat(
            chat_id=chat_id,
            YouMessage=YouMessage,
            AiMessage=AiMessage,
            data_relevant=data_relevant,
            source_file=source_file
        )
        session.add(new_user)
        session.commit()
        return new_user.id
        session.close()

def getDetailChatByChatId(id: int) -> detail_chat:
    try:
        engine = cf.get_db_engine()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            try:
                chat = session.query(detail_chat).filter(detail_chat.id == id).one_or_none()
                return chat
            except:
                session.close()
                return False
    except:
        engine = cf.get_db_engine1()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session:
            try:
                chat = session.query(detail_chat.id,detail_chat.data_relevant,detail_chat.source_file).filter(detail_chat.id == id).one_or_none()
                session.commit()
                session.close()
                return chat
            except:
                session.close()
                return False


def delete_chat_detail(chat_name: str) -> bool:
 try:
  engine = cf.get_db_engine()
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  with Session() as session:
    try:
        detail_chat2 = session.query(detail_chat).filter(detail_chat.chat_id == chat_history.id).filter(chat_history.name_chat == chat_name)
        session.query(detail_chat).filter(detail_chat.chat_id == chat_history.id).filter(chat_history.name_chat == chat_name).delete(synchronize_session=False)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False
 except:
  engine = cf.get_db_engine1()
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  with Session() as session:
    try:
        session.query(detail_chat).filter(detail_chat.chat_id == chat_history.id).filter(chat_history.name_chat == chat_name).delete(synchronize_session=False)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False
def delete_chat_detail_by_id(id_chat_detail: int) -> bool:
 try:
  engine = cf.get_db_engine()
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  with Session() as session:
    try:

        session.query(detail_chat).filter(detail_chat.id == id_chat_detail).delete(synchronize_session=False)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False
 except:
  engine = cf.get_db_engine1()
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  with Session() as session:
    try:
        session.query(detail_chat).filter(detail_chat.chat_id == id_chat_detail).delete(synchronize_session=False)
        session.commit()
        session.close()
        return True
    except:
        session.close()
        return False