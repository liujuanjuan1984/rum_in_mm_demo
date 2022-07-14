import datetime
import logging

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

logger = logging.getLogger(__name__)


class BaseDB:
    def __init__(self, db_name, echo, reset):
        # 创建数据库
        engine = create_engine(db_name, echo=echo, connect_args={"check_same_thread": False})
        if reset:
            Base.metadata.drop_all(engine)
        # 创建表
        Base.metadata.create_all(engine)
        # 创建会话
        self.Session = sessionmaker(bind=engine, autoflush=False)
        self.session = self.Session()
        logger.debug(f"init db, name: {db_name}, echo: {echo}, reset: {reset}")

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        logger.debug("db commit")

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add(self, obj):
        """Adds this model to the db (through db.session)"""
        self.session.add(obj)
        self.__commit()
        return self

    def commit(self):
        self.__commit()
        return self

    def delete(self, obj):
        """Deletes this model from the db (through db.session)"""
        self.session.delete(self)
        self.__commit()


class KeyStore(Base):
    """each mixin_id got a keystore"""

    __tablename__ = "keystores"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    mixin_id = Column(String(36))
    addr = Column(String, default=None)
    keystore = Column(String)
    groups = Column(String, default=None)
    created_at = Column(String, default=str(datetime.datetime.now()))
    updated_at = Column(String, default=str(datetime.datetime.now()))

    def __init__(self, obj):
        super().__init__(**obj)


class BotComments(Base):
    """msgs from bot users which needs to be update rss or reply or send to rum groups."""

    logger.debug("BotComments")
    __tablename__ = "bot_comments"
    id = Column(Integer, unique=True, primary_key=True, index=True)
    message_id = Column(String(36), unique=True)
    is_reply = Column(Boolean, default=None)
    is_to_rum = Column(Boolean, default=None)  # 是否转发到rum，不需要转发为None；需要转发但没发，设置为False，转发成功设为True
    quote_message_id = Column(String(36), default=None)
    conversation_id = Column(String(36), default=None)
    user_id = Column(String(36), default=None)
    text = Column(String, default=None)
    category = Column(String(36), default=None)
    timestamp = Column(String, default=None)  # 消息的发送时间
    created_at = Column(String, default=str(datetime.datetime.now()))
    updated_at = Column(String, default=str(datetime.datetime.now()))

    def __init__(self, obj):
        super().__init__(**obj)
