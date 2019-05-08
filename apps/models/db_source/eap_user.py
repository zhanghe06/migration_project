# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, TIMESTAMP, Unicode, text
from sqlalchemy.dialects.mssql.base import BIT, UNIQUEIDENTIFIER
from apps.databases.db_source import db


Base = db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class EAPUser(Base):
    __tablename__ = 'EAP_User'

    id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=text("(newid())"))
    Code = Column(Unicode(50), index=True)
    name = Column(Unicode(50))
    email = Column(Unicode(20))
    IsUsed = Column(BIT, server_default=text("(0)"))
    password = Column(Unicode(50))
    isAdmin = Column(BIT, server_default=text("(0)"))
    isStoped = Column(BIT, server_default=text("(0)"))
    mobile = Column(Unicode(20))
    OrderNum = Column(Integer, nullable=False)
    AuthState = Column(Integer, server_default=text("(0)"))
    IdPerson = Column(UNIQUEIDENTIFIER, server_default=text("(newid())"))
    PersonName = Column(Unicode(50))
    lastLoginDate = Column(String(10, u'Chinese_PRC_CI_AS'))
    createdDate = Column(String(10, u'Chinese_PRC_CI_AS'))
    ts = Column(TIMESTAMP)
    updated = Column(DateTime)
    updatedBy = Column(Unicode(32))
    Memo = Column(Unicode(50))
    issystem = Column(BIT)
    IdMarketingOrgan = Column(UNIQUEIDENTIFIER, index=True)
    ShowNewFuncIntro = Column(Integer, nullable=False, server_default=text("((1))"))
