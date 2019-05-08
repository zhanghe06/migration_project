# coding: utf-8
from sqlalchemy import Column, Integer, String, TIMESTAMP, Unicode
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import db


Base = db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class AAInventoryLocation(Base):
    __tablename__ = 'AA_InventoryLocation'

    id = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False, unique=True)
    code = Column(Unicode(32), index=True)
    name = Column(Unicode(200), index=True)
    shorthand = Column(Unicode(50))
    isEndNode = Column(Integer)
    depth = Column(Integer)
    memo = Column(Unicode(50))
    disabled = Column(Integer)
    madeDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    ts = Column(TIMESTAMP)
    updated = Column(String(19, u'Chinese_PRC_CI_AS'))
    idwarehouse = Column(UNIQUEIDENTIFIER, index=True)
    updatedBy = Column(Unicode(32))
    idparent = Column(UNIQUEIDENTIFIER, index=True)
    inId = Column(Unicode(560))
    createdTime = Column(String(19, u'Chinese_PRC_CI_AS'))
