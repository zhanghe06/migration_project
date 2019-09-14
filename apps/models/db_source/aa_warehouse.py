# coding: utf-8
from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, Unicode
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import source_db


Base = source_db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class AAWarehouse(Base):
    __tablename__ = 'AA_Warehouse'

    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    code = Column(Unicode(32), index=True)
    name = Column(Unicode(200), index=True)
    address = Column(Unicode(200))
    hasPosition = Column(Integer)
    memo = Column(Unicode(50))
    disabled = Column(Integer)
    madeDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    ts = Column(TIMESTAMP)
    updated = Column(String(19, u'Chinese_PRC_CI_AS'))
    updatedBy = Column(Unicode(32))
    idadmin = Column(UNIQUEIDENTIFIER, index=True)
    priuserdefnvc1 = Column(Unicode(500))
    priuserdefdecm1 = Column(Numeric(28, 14))
    priuserdefnvc2 = Column(Unicode(500))
    priuserdefdecm2 = Column(Numeric(28, 14))
    priuserdefnvc3 = Column(Unicode(500))
    priuserdefdecm3 = Column(Numeric(28, 14))
    priuserdefnvc4 = Column(Unicode(500))
    priuserdefdecm4 = Column(Numeric(28, 14))
    priuserdefnvc5 = Column(Unicode(500))
    priuserdefdecm5 = Column(Numeric(28, 14))
    involveatp = Column(Integer)
    floorstocks = Column(Integer)
    createdTime = Column(String(19, u'Chinese_PRC_CI_AS'))
    idMarketingOrgan = Column(UNIQUEIDENTIFIER, index=True)
    shorthand = Column(Unicode(50))
    DistributionWay = Column(UNIQUEIDENTIFIER)
