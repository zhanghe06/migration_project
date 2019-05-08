# coding: utf-8
from sqlalchemy import Column, Integer, TIMESTAMP, Unicode, text
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import db


Base = db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class EapEnumItem(Base):
    __tablename__ = 'eap_EnumItem'

    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    idEnum = Column(UNIQUEIDENTIFIER)
    Code = Column(Unicode(50))
    Name = Column(Unicode(300))
    CustomUse = Column(Integer, server_default=text("(1)"))
    IsExtend = Column(Integer, nullable=False, server_default=text("(0)"))
    IsDeleted = Column(Integer, nullable=False, server_default=text("(0)"))
    position = Column(Integer)
    autoid = Column(Integer, nullable=False, index=True)
    TS = Column(TIMESTAMP, nullable=False)
    ExpressionName = Column(Unicode(60))
