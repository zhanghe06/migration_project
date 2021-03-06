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


class SASaleDeliveryB(Base):
    __tablename__ = 'SA_SaleDelivery_b'
    __table_args__ = (
        Index('index_SA_SaleDelivery_b_idSaleDeliveryDTO__origSettleAmount', 'idSaleDeliveryDTO', 'origSettleAmount'),
        Index('IDX_Sa_SaleDelivery_b_PromotionSingle', 'PromotionSingleTypeID', 'PromotionSingleVoucherCode'),
        Index('index_SA_SaleDelivery_b_idSaleDeliveryDTO__taxAmount', 'idSaleDeliveryDTO', 'taxAmount'),
        Index('IDX_Sa_SaleDelivery_b_PromotionPresent', 'PromotionPresentTypeID', 'PromotionPresentVoucherCode'),
        Index('_dta_index_SA_SaleDelivery_b_idSaleDeliveryDTO_id_saleOrderId', 'idSaleDeliveryDTO', 'updated', 'id', 'saleOrderId'),
        Index('Index_1', 'idwarehouse', 'idSaleDeliveryDTO')
    )

    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    code = Column(Unicode(30))
    name = Column(Unicode(200))
    isNoModify = Column(Unicode(1000))
    quantity = Column(Numeric(28, 14))
    quantity2 = Column(Numeric(28, 14))
    unitExchangeRate = Column(Numeric(28, 14))
    baseQuantity = Column(Numeric(28, 14))
    subQuantity = Column(Numeric(28, 14))
    compositionQuantity = Column(Unicode(100))
    origPrice = Column(Numeric(28, 14))
    price = Column(Numeric(28, 14))
    basePrice = Column(Numeric(28, 14))
    discountRate = Column(Numeric(28, 14))
    origDiscountPrice = Column(Numeric(28, 14))
    discountPrice = Column(Numeric(28, 14))
    baseDiscountPrice = Column(Numeric(28, 14))
    taxRate = Column(Numeric(28, 14))
    origTaxPrice = Column(Numeric(28, 14))
    taxPrice = Column(Numeric(28, 14))
    baseTaxPrice = Column(Numeric(28, 14))
    origDiscountAmount = Column(Numeric(28, 14))
    discountAmount = Column(Numeric(28, 14))
    origTax = Column(Numeric(28, 14))
    tax = Column(Numeric(28, 14))
    origTaxAmount = Column(Numeric(28, 14))
    taxAmount = Column(Numeric(28, 14))
    origDiscount = Column(Numeric(28, 14))
    discount = Column(Numeric(28, 14))
    costPrice = Column(Numeric(28, 14))
    costAmount = Column(Numeric(28, 14))
    receiveVoucherCode = Column(Unicode(50))
    receiveVoucherId = Column(UNIQUEIDENTIFIER, index=True)
    receiveVoucherDetailId = Column(UNIQUEIDENTIFIER)
    saleOrderId = Column(UNIQUEIDENTIFIER)
    saleOrderCode = Column(Unicode(30))
    saleOrderDetailId = Column(UNIQUEIDENTIFIER)
    batch = Column(Unicode(50))
    adjustAmount = Column(Numeric(28, 14))
    expiryDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    deliveryDate = Column(String(19, u'Chinese_PRC_CI_AS'))
    isPresent = Column(Integer)
    sourceVoucherId = Column(UNIQUEIDENTIFIER, index=True)
    sourceVoucherDetailId = Column(UNIQUEIDENTIFIER, index=True)
    counteractQuntity = Column(Numeric(28, 14))
    counteractQuntity2 = Column(Numeric(28, 14))
    returnQuntity = Column(Numeric(28, 14))
    returnQuntity2 = Column(Numeric(28, 14))
    saleoutquantity2 = Column(Numeric(28, 14))
    saleOutQuantity = Column(Numeric(28, 14))
    idSaleDeliveryDTO = Column(UNIQUEIDENTIFIER, index=True)
    idwarehouse = Column(UNIQUEIDENTIFIER, index=True)
    invoiceQuantity2 = Column(Numeric(28, 14))
    invoiceQuantity = Column(Numeric(28, 14))
    settleAmount = Column(Numeric(28, 14))
    idinventory = Column(UNIQUEIDENTIFIER, index=True)
    origSettleAmount = Column(Numeric(28, 14))
    isCancel = Column(UNIQUEIDENTIFIER)
    origExpenseAmount = Column(Numeric(28, 14))
    expenseAmount = Column(Numeric(28, 14))
    idunit2 = Column(UNIQUEIDENTIFIER)
    isSaleOut = Column(UNIQUEIDENTIFIER)
    inventoryLocation = Column(Unicode(50))
    sourceVoucherCode = Column(Unicode(50))
    idbaseunit = Column(UNIQUEIDENTIFIER)
    taxFlag = Column(Integer)
    isManualCost = Column(Integer)
    idunit = Column(UNIQUEIDENTIFIER)
    lastmodifiedfield = Column(Unicode(50))
    idsubunit = Column(UNIQUEIDENTIFIER)
    inventoryBarCode = Column(Unicode(200))
    partnerInventoryCode = Column(Unicode(50))
    createdtime = Column(String(19, u'Chinese_PRC_CI_AS'))
    sequencenumber = Column(Integer)
    ts = Column(TIMESTAMP)
    updated = Column(String(19, u'Chinese_PRC_CI_AS'), index=True)
    updatedBy = Column(Unicode(32))
    idsourcevouchertype = Column(UNIQUEIDENTIFIER, index=True)
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
    priuserdefnvc1 = Column(Unicode(500))
    priuserdefdecm1 = Column(Numeric(28, 14), index=True)
    priuserdefnvc2 = Column(Unicode(500))
    priuserdefdecm2 = Column(Numeric(28, 14))
    priuserdefnvc3 = Column(Unicode(500))
    priuserdefdecm3 = Column(Numeric(28, 14))
    priuserdefnvc4 = Column(Unicode(500))
    priuserdefdecm4 = Column(Numeric(28, 14))
    pubuserdefnvc1 = Column(Unicode(500))
    pubuserdefdecm1 = Column(Numeric(28, 14))
    pubuserdefnvc2 = Column(Unicode(500))
    pubuserdefdecm2 = Column(Numeric(28, 14))
    pubuserdefnvc3 = Column(Unicode(500))
    pubuserdefdecm3 = Column(Numeric(28, 14))
    pubuserdefnvc4 = Column(Unicode(500))
    pubuserdefdecm4 = Column(Numeric(28, 14))
    AvailableQuantity = Column(Numeric(28, 14))
    ExistingQuantity = Column(Numeric(28, 14))
    partnerInventoryName = Column(Unicode(50))
    idproject = Column(UNIQUEIDENTIFIER, index=True)
    docid = Column(UNIQUEIDENTIFIER)
    virtualBaseQuantity = Column(Numeric(28, 14))
    virtualBaseAmount = Column(Numeric(28, 14))
    sentBaseQuantityAssociated = Column(Numeric(28, 14))
    sentBaseAmountAssociated = Column(Numeric(28, 14))
    backSentAmount = Column(Numeric(28, 14))
    backSentQuantity = Column(Numeric(28, 14))
    associatedDocIDs = Column(Unicode(400))
    Retailprice = Column(Numeric(28, 14))
    DistributionQuantity = Column(Numeric(28, 14))
    DistributionQuantity2 = Column(Numeric(28, 14))
    BoxNumber = Column(Unicode(50))
    OrigInvoiceTaxAmount = Column(Numeric(28, 14))
    PriceStrategyTypeName = Column(Unicode(200))
    PriceStrategyTypeId = Column(UNIQUEIDENTIFIER)
    PriceStrategySchemeIds = Column(Unicode(1000))
    PriceStrategySchemeNames = Column(Unicode(400))
    PromotionVoucherCodes = Column(Unicode(400))
    PromotionVoucherIds = Column(Unicode(400))
    IsMemberIntegral = Column(Integer)
    IsPromotionPresent = Column(Integer)
    PromotionPresentVoucherID = Column(UNIQUEIDENTIFIER)
    PromotionPresentVoucherCode = Column(Unicode(50))
    PromotionPresentTypeID = Column(UNIQUEIDENTIFIER)
    PromotionSingleTypeID = Column(UNIQUEIDENTIFIER)
    PromotionSingleVoucherID = Column(UNIQUEIDENTIFIER)
    PromotionSingleVoucherCode = Column(Unicode(50))
    PromotionPresentGroupID = Column(Unicode(150))
    PromotionSingleGroupID = Column(Unicode(150))
    CashbackWay = Column(UNIQUEIDENTIFIER)
    SuperSourceVoucherTypeCode = Column(Unicode(50))
    ProductionDate = Column(String(19, u'Chinese_PRC_CI_AS'))
