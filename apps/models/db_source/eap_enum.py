# coding: utf-8
from sqlalchemy import Column, Integer, String, TIMESTAMP, Unicode, text
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import source_db


Base = source_db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class EapEnum(Base):
    __tablename__ = 'eap_Enum'

    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    Name = Column(Unicode(50))
    Title = Column(Unicode(200))
    Custom = Column(Integer, nullable=False, server_default=text("(0)"))
    Customuse = Column(Integer, server_default=text("(1)"))
    autoid = Column(Integer, nullable=False, index=True)
    TS = Column(TIMESTAMP, nullable=False)
    Code = Column(String(200, u'Chinese_PRC_CI_AS'))
