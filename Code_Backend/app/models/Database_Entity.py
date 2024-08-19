from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255))
    access_token = Column(Text)
    refresh_token = Column(Text)
    expires_at = Column(DateTime)

    chat_histories = relationship("ChatHistory", back_populates="user")
    user_logins = relationship("UserLogin", back_populates="user")
    user_infos = relationship("UserInfo", back_populates="user")

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(255), ForeignKey('users.email'))
    name_chat = Column(String(255), unique=True)

    user = relationship("User", back_populates="chat_histories")
    detail_chats = relationship("DetailChat", back_populates="chat_history")

class UserLogin(Base):
    __tablename__ = 'user_login'

    id = Column(Integer, primary_key=True,autoincrement=True)
    user_email = Column(String(100), ForeignKey('users.email'), primary_key=True)
    user_session_id = Column(String(100), primary_key=True)
    
    user = relationship("User", back_populates="user_logins")

class UserInfo(Base):
    __tablename__ = 'user_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Text)
    email = Column(String(255), ForeignKey('users.email'), unique=True)
    display_name = Column(Text)
    photo_url = Column(Text)
    
    user = relationship("User", back_populates="user_infos")

class DetailChat(Base):
    __tablename__ = 'detail_chat'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat_history.id'))
    YouMessage = Column(Text)
    AiMessage = Column(Text)
    data_relevant = Column(Text)
    source_file = Column(Text)

    chat_history = relationship("ChatHistory", back_populates="detail_chats")

class OTP(Base):
    __tablename__ = 'otp'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    otp = Column(String(6), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())