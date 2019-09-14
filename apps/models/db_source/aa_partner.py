# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, Numeric, String, TIMESTAMP, Unicode
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import source_db


Base = source_db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class AAPartner(Base):
    __tablename__ = 'AA_Partner'
    __table_args__ = (
        Index('IX_AA_Partner_PartnerType', 'disabled', 'partnerType', 'id', 'idpartnerclass'),
        Index('IX_AA_Partner_IdParent_Code', 'disabled', 'idpartnerclass', 'code', 'id')
    )

    id = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False, unique=True)
    code = Column(Unicode(32), index=True)
    name = Column(Unicode(200), index=True)
    partnerAbbName = Column(Unicode(100))
    shortHand = Column(Unicode(100))
    partnerType = Column(UNIQUEIDENTIFIER)
    priceGrade = Column(UNIQUEIDENTIFIER)
    taxRate = Column(UNIQUEIDENTIFIER)
    representative = Column(Unicode(50))
    accbank = Column(UNIQUEIDENTIFIER)
    bankAccount = Column(Unicode(50))
    taxRegcode = Column(Unicode(50))
    saleCreditLine = Column(Numeric(28, 14))
    saleSettleStyle = Column(UNIQUEIDENTIFIER)
    purchaseSettleStyle = Column(UNIQUEIDENTIFIER)
    saleCreditDays = Column(Numeric(28, 14))
    purchaseCreditDays = Column(Numeric(28, 14))
    saleStartDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    saleSpaceMonth = Column(Integer)
    saleCheckMonth = Column(Integer)
    saleCheckDate = Column(Integer)
    purchaseStartDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    purchaseSpaceMonth = Column(Integer)
    purchaseCheckMonth = Column(Integer)
    purchaseCheckDate = Column(Integer)
    customeraddressphone = Column(Unicode(250))
    aRBalance = Column(Numeric(28, 14))
    aPBalance = Column(Numeric(28, 14))
    disabled = Column(Integer)
    madeDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    ts = Column(TIMESTAMP)
    updated = Column(String(19, u'Chinese_PRC_CI_AS'))
    updatedBy = Column(Unicode(32))
    idpartnerclass = Column(UNIQUEIDENTIFIER, index=True)
    iddistrict = Column(UNIQUEIDENTIFIER, index=True)
    idsaleman = Column(UNIQUEIDENTIFIER, index=True)
    idsaledepartment = Column(UNIQUEIDENTIFIER, index=True)
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
    isContainTaxOnPurchase = Column(Integer)
    HasEverChanged = Column(Unicode(32))
    idsettlementPartner = Column(UNIQUEIDENTIFIER, index=True)
    codeSettlementPartner = Column(Unicode(32))
    createdTime = Column(String(19, u'Chinese_PRC_CI_AS'))
    AdvRBalance = Column(Numeric(28, 14))
    AdvPBalance = Column(Numeric(28, 14))
    addressJC = Column(Unicode(200))
    ShipmentAddress = Column(Unicode(200))
    Contact = Column(Unicode(50))
    MobilePhone = Column(Unicode(30))
    TelephoneNo = Column(Unicode(100))
    Fax = Column(Unicode(20))
    EmailAddr = Column(Unicode(100))
    QqNo = Column(Unicode(50))
    MsnAddress = Column(Unicode(50))
    UuNo = Column(Unicode(50))
    creditBalance = Column(Numeric(28, 14))
    extendedAccounts = Column(Numeric(28, 14))
    idPmarketingOrgan = Column(UNIQUEIDENTIFIER)
    idMarketingOrgan = Column(UNIQUEIDENTIFIER, index=True)
    CustomerType = Column(UNIQUEIDENTIFIER)
    SellCustomer = Column(Integer)
    MadeRecordDate = Column(DateTime)
    Position = Column(Unicode(20))
    RunShop = Column(Integer)
    CheckAddress = Column(Unicode(200))
    CustomerAddress = Column(Unicode(200))
    Birthday = Column(DateTime)
    AutoCreateMember = Column(Integer)
    idMemberType = Column(UNIQUEIDENTIFIER)
