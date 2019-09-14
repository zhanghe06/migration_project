# coding: utf-8
from sqlalchemy import Column, Index, Integer, Numeric, String, TIMESTAMP, Unicode
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from apps.databases.db_source import source_db


Base = source_db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_source'


class STCurrentStock(Base):
    __tablename__ = 'ST_CurrentStock'
    __table_args__ = (
        Index('ix_ST_CurrentStock_4', 'idinventory', 'idwarehouse', 'batch'),
    )

    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    code = Column(Unicode(30))
    name = Column(Unicode(200))
    batch = Column(Unicode(50))
    expiryDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    baseQuantity = Column(Numeric(28, 14))
    subQuantity = Column(Numeric(28, 14))
    canUseBaseQuantity = Column(Numeric(28, 14))
    canUseSubQuantity = Column(Numeric(28, 14))
    onWayBaseQuantity = Column(Numeric(28, 14))
    onWaySubQuantity = Column(Numeric(28, 14))
    forDispatchBaseQuantity = Column(Numeric(28, 14))
    forDispatchSubQuantity = Column(Numeric(28, 14))
    purchaseOrderOnWayBaseQuantity = Column(Numeric(28, 14))
    purchaseOrderOnWaySubQuantity = Column(Numeric(28, 14))
    purchaseArrivalBaseQuantity = Column(Numeric(28, 14))
    purchaseArrivalSubQuantity = Column(Numeric(28, 14))
    purchaseForReceiveBaseQuantity = Column(Numeric(28, 14))
    purchaseForReceiveSubQuantity = Column(Numeric(28, 14))
    onProducingBaseQuantity = Column(Numeric(28, 14))
    onProducingSubQuantity = Column(Numeric(28, 14))
    productForReceiveBaseQuantity = Column(Numeric(28, 14))
    productForReceiveSubQuantity = Column(Numeric(28, 14))
    transOnWayBaseQuantity = Column(Numeric(28, 14))
    transOnWaySubQuantity = Column(Numeric(28, 14))
    transForDispatchBaseQuantity = Column(Numeric(28, 14))
    transForDispatchSubQuantity = Column(Numeric(28, 14))
    otherOnWayBaseQuantity = Column(Numeric(28, 14))
    otherOnWaySubQuantity = Column(Numeric(28, 14))
    otherForDispatchBaseQuantity = Column(Numeric(28, 14))
    otherForDispatchSubQuantity = Column(Numeric(28, 14))
    forSaleOrderBaseQuantity = Column(Numeric(28, 14))
    forSaleOrderSubQuantity = Column(Numeric(28, 14))
    saleDeliveryBaseQuantity = Column(Numeric(28, 14))
    saleDeliverySubQuantity = Column(Numeric(28, 14))
    forSaleDispatchBaseQuantity = Column(Numeric(28, 14))
    forSaleDispatchSubQuantity = Column(Numeric(28, 14))
    materialForSendBaseQuantity = Column(Numeric(28, 14))
    materialForSendSubQuantity = Column(Numeric(28, 14))
    receiveVoucherCode = Column(Unicode(50))
    receiveVoucherDetailId = Column(UNIQUEIDENTIFIER)
    receiveVoucherId = Column(UNIQUEIDENTIFIER)
    voucherQuantity = Column(Numeric(28, 14))
    voucherQuantity2 = Column(Numeric(28, 14))
    preBaseQuantity = Column(Numeric(28, 14))
    preSubQuantity = Column(Numeric(28, 14))
    lowQuantity = Column(Numeric(28, 14))
    topQuantity = Column(Numeric(28, 14))
    recordDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    changeRate = Column(Numeric(28, 14))
    isCarriedForwardOut = Column(Integer)
    isCarriedForwardIn = Column(Integer)
    createdtime = Column(String(19, u'Chinese_PRC_CI_AS'))
    sequencenumber = Column(Integer)
    ts = Column(TIMESTAMP)
    updated = Column(String(19, u'Chinese_PRC_CI_AS'), index=True)
    updatedBy = Column(Unicode(32))
    idBatchDispatchDTO = Column(UNIQUEIDENTIFIER)
    idwarehouse = Column(UNIQUEIDENTIFIER, index=True)
    idbaseunit = Column(UNIQUEIDENTIFIER)
    idsubunit = Column(UNIQUEIDENTIFIER)
    idinventory = Column(UNIQUEIDENTIFIER, index=True)
    idvoucherunit = Column(UNIQUEIDENTIFIER)
    idvoucherunit2 = Column(UNIQUEIDENTIFIER)
    freeItem0 = Column(Unicode(300))
    freeItem1 = Column(Unicode(300))
    freeItem2 = Column(Unicode(300))
    freeItem3 = Column(Unicode(300))
    freeItem4 = Column(Unicode(300))
    freeItem5 = Column(Unicode(300))
    freeItem6 = Column(Unicode(300))
    freeItem7 = Column(Unicode(300))
    freeItem8 = Column(Unicode(300))
    freeItem9 = Column(Unicode(300))
    ProduceForDispatchBaseQuantity = Column(Numeric(28, 14))
    ProduceForDispatchSubQuantity = Column(Numeric(28, 14))
    IdMarketingOrgan = Column(UNIQUEIDENTIFIER)
    forEShopDispatchBaseQuantity = Column(Numeric(28, 14))
    forEShopDispatchSubQuantity = Column(Numeric(28, 14))
    stockRequestBaseQuantity = Column(Numeric(28, 14))
    stockRequestSubQuantity = Column(Numeric(28, 14))
    productionDate = Column(String(19, u'Chinese_PRC_CI_AS'))
