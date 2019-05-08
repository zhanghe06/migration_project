# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Index, Integer, Numeric, String, text
from apps.databases.db_target import db


Base = db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_target'


class BankAccount(Base):
    __tablename__ = 'bank_account'

    id = Column(Integer, primary_key=True)
    bank_name = Column(String(100), nullable=False, server_default=text("''"))
    type_bank = Column(Integer, nullable=False, server_default=text("'0'"))
    initial_balance = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    closing_balance = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BankAccountItems(Base):
    __tablename__ = 'bank_account_items'
    __table_args__ = (
        Index('type_current', 'type_current', 'cid'),
    )

    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    type_current = Column(Integer, nullable=False, server_default=text("'0'"))
    cid = Column(Integer, nullable=False, server_default=text("'0'"))
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_account = Column(Integer, nullable=False, server_default=text("'0'"))
    amount = Column(Numeric(8, 2), nullable=False, server_default=text("'0.00'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BuyerOrder(Base):
    __tablename__ = 'buyer_order'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_order = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    delivery_way = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_effect = Column(Integer, nullable=False, server_default=text("'0'"))
    status_completion = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    audit_time = Column(DateTime)
    effect_time = Column(DateTime)
    completion_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BuyerOrderItems(Base):
    __tablename__ = 'buyer_order_items'

    id = Column(Integer, primary_key=True)
    buyer_order_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_company_name = Column(String(100), nullable=False, server_default=text("''"))
    custom_production_brand = Column(String(32), nullable=False, server_default=text("''"))
    custom_production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    delivery_time = Column(String(128), nullable=False, server_default=text("''"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CashAccount(Base):
    __tablename__ = 'cash_account'

    id = Column(Integer, primary_key=True)
    cash_name = Column(String(100), nullable=False, server_default=text("''"))
    initial_balance = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    closing_balance = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CashAccountItems(Base):
    __tablename__ = 'cash_account_items'
    __table_args__ = (
        Index('type_current', 'type_current', 'cid'),
    )

    id = Column(Integer, primary_key=True)
    cash_id = Column(Integer, nullable=False, server_default=text("'0'"))
    type_current = Column(Integer, nullable=False, server_default=text("'0'"))
    cid = Column(Integer, nullable=False, server_default=text("'0'"))
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_account = Column(Integer, nullable=False, server_default=text("'0'"))
    amount = Column(Numeric(8, 2), nullable=False, server_default=text("'0.00'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Catalogue(Base):
    __tablename__ = 'catalogue'
    __table_args__ = (
        Index('production_brand', 'production_brand', 'production_model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, index=True, server_default=text("''"))
    production_label = Column(String(64), nullable=False, server_default=text("''"))
    production_brand_old = Column(String(32), nullable=False, server_default=text("''"))
    production_model_old = Column(String(64), nullable=False, index=True, server_default=text("''"))
    production_class = Column(String(32), nullable=False, server_default=text("''"))
    ind = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    oud = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    wid = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    speed_g = Column(Numeric(6, 0), nullable=False, server_default=text("'0'"))
    speed_o = Column(Numeric(6, 0), nullable=False, server_default=text("'0'"))
    weight = Column(Numeric(8, 3), nullable=False, server_default=text("'0.000'"))
    serie = Column(String(32), nullable=False, server_default=text("''"))
    accuracy = Column(String(64), nullable=False, server_default=text("''"))
    preload = Column(String(64), nullable=False, server_default=text("''"))
    seal = Column(String(64), nullable=False, server_default=text("''"))
    angle = Column(String(64), nullable=False, server_default=text("''"))
    r_size = Column(String(64), nullable=False, server_default=text("''"))
    r_matel = Column(String(64), nullable=False, server_default=text("''"))
    assembly_no = Column(String(64), nullable=False, server_default=text("''"))
    assembly_type = Column(String(64), nullable=False, server_default=text("''"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    tag = Column(String(256), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, server_default=text("''"))
    main_id = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    company_address = Column(String(100), nullable=False, server_default=text("''"))
    company_site = Column(String(100), nullable=False, server_default=text("''"))
    company_tel = Column(String(100), nullable=False, server_default=text("''"))
    company_fax = Column(String(100), nullable=False, server_default=text("''"))
    company_email = Column(String(100), nullable=False, server_default=text("''"))
    company_type = Column(Integer, nullable=False, server_default=text("'0'"))
    owner_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CustomerContact(Base):
    __tablename__ = 'customer_contact'

    id = Column(Integer, primary_key=True)
    cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    name = Column(String(20), nullable=False, server_default=text("''"))
    salutation = Column(String(20), nullable=False, server_default=text("''"))
    mobile = Column(String(20), nullable=False, server_default=text("''"))
    tel = Column(String(20), nullable=False, server_default=text("''"))
    fax = Column(String(20), nullable=False, server_default=text("''"))
    email = Column(String(60), nullable=False, server_default=text("''"))
    department = Column(String(20), nullable=False, server_default=text("''"))
    address = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    status_default = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CustomerInvoice(Base):
    __tablename__ = 'customer_invoice'

    cid = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    company_tax_id = Column(String(20), nullable=False, server_default=text("''"))
    company_address = Column(String(100), nullable=False, server_default=text("''"))
    company_tel = Column(String(100), nullable=False, server_default=text("''"))
    company_bank_name = Column(String(100), nullable=False, server_default=text("''"))
    company_bank_account = Column(String(100), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    sales_order_id = Column(Integer, index=True, server_default=text("'0'"))
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_company_name = Column(String(100), nullable=False, server_default=text("''"))
    customer_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    type_delivery = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_delivery = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    warehouse_id = Column(Integer, nullable=False)
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_confirm = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    audit_time = Column(DateTime)
    confirm_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class DeliveryItems(Base):
    __tablename__ = 'delivery_items'

    id = Column(Integer, primary_key=True)
    delivery_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    sales_order_id = Column(Integer, index=True, server_default=text("'0'"))
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_company_name = Column(String(100), nullable=False, server_default=text("''"))
    custom_production_brand = Column(String(32), nullable=False, server_default=text("''"))
    custom_production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(16), nullable=False, server_default=text("''"))
    production_model = Column(String(32), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    warehouse_id = Column(Integer, nullable=False)
    rack_id = Column(Integer, nullable=False)
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(8, 2), nullable=False, server_default=text("'0.00'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Enquiry(Base):
    __tablename__ = 'enquiry'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_enquiry = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    delivery_way = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_order = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    expiry_date = Column(Date, nullable=False)
    audit_time = Column(DateTime)
    order_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class EnquiryItems(Base):
    __tablename__ = 'enquiry_items'

    id = Column(Integer, primary_key=True)
    enquiry_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True)
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_company_name = Column(String(100), nullable=False, server_default=text("''"))
    enquiry_production_model = Column(String(64), nullable=False, server_default=text("''"))
    enquiry_quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    delivery_time = Column(String(128), nullable=False, server_default=text("''"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    status_ordered = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    warehouse_id = Column(Integer, nullable=False)
    warehouse_name = Column(String(100), nullable=False, server_default=text("''"))
    rack_id = Column(Integer, nullable=False)
    rack_name = Column(String(16), nullable=False, server_default=text("''"))
    stock_qty_initial = Column(Integer, nullable=False, server_default=text("'0'"))
    stock_qty_current = Column(Integer, nullable=False, server_default=text("'0'"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Production(Base):
    __tablename__ = 'production'
    __table_args__ = (
        Index('production_brand', 'production_brand', 'production_model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, nullable=False, server_default=text("'0'"))
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, index=True, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    production_class = Column(String(32), nullable=False, server_default=text("''"))
    ind = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    oud = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    wid = Column(Numeric(4, 0), nullable=False, server_default=text("'0'"))
    speed_g = Column(Numeric(6, 0), nullable=False, server_default=text("'0'"))
    speed_o = Column(Numeric(6, 0), nullable=False, server_default=text("'0'"))
    weight = Column(Numeric(8, 3), nullable=False, server_default=text("'0.000'"))
    serie = Column(String(32), nullable=False, server_default=text("''"))
    accuracy = Column(String(64), nullable=False, server_default=text("''"))
    preload = Column(String(64), nullable=False, server_default=text("''"))
    seal = Column(String(64), nullable=False, server_default=text("''"))
    angle = Column(String(64), nullable=False, server_default=text("''"))
    r_size = Column(String(64), nullable=False, server_default=text("''"))
    r_matel = Column(String(64), nullable=False, server_default=text("''"))
    assembly_no = Column(String(64), nullable=False, server_default=text("''"))
    assembly_type = Column(String(64), nullable=False, server_default=text("''"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    tag = Column(String(256), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ProductionSensitive(Base):
    __tablename__ = 'production_sensitive'
    __table_args__ = (
        Index('customer_cid_2', 'customer_cid', 'production_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_company_name = Column(String(100), nullable=False, server_default=text("''"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    buyer_order_id = Column(Integer, index=True, server_default=text("'0'"))
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_company_name = Column(String(100), nullable=False, server_default=text("''"))
    supplier_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    type_purchase = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_purchase = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    warehouse_id = Column(Integer, nullable=False)
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_confirm = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    audit_time = Column(DateTime)
    confirm_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class PurchaseItems(Base):
    __tablename__ = 'purchase_items'

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    buyer_order_id = Column(Integer, index=True, server_default=text("'0'"))
    supplier_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    supplier_company_name = Column(String(100), nullable=False, server_default=text("''"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(16), nullable=False, server_default=text("''"))
    production_model = Column(String(32), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    warehouse_id = Column(Integer, nullable=False)
    rack_id = Column(Integer, nullable=False)
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(8, 2), nullable=False, server_default=text("'0.00'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Quotation(Base):
    __tablename__ = 'quotation'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_quotation = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    delivery_way = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_order = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    expiry_date = Column(Date, nullable=False)
    audit_time = Column(DateTime)
    order_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class QuotationItems(Base):
    __tablename__ = 'quotation_items'

    id = Column(Integer, primary_key=True)
    quotation_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True)
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_company_name = Column(String(100), nullable=False, server_default=text("''"))
    enquiry_production_model = Column(String(64), nullable=False, server_default=text("''"))
    enquiry_quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    delivery_time = Column(String(128), nullable=False, server_default=text("''"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    status_ordered = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Rack(Base):
    __tablename__ = 'rack'

    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, nullable=False)
    name = Column(String(16), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class SalesOrder(Base):
    __tablename__ = 'sales_order'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_contact_id = Column(Integer, nullable=False, server_default=text("'0'"))
    amount_production = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_shipping = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_adjustment = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    amount_order = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    delivery_way = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    audit_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_audit = Column(Integer, nullable=False, server_default=text("'0'"))
    status_effect = Column(Integer, nullable=False, server_default=text("'0'"))
    status_completion = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    audit_time = Column(DateTime)
    effect_time = Column(DateTime)
    completion_time = Column(DateTime)
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class SalesOrderItems(Base):
    __tablename__ = 'sales_order_items'

    id = Column(Integer, primary_key=True)
    sales_order_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    customer_company_name = Column(String(100), nullable=False, server_default=text("''"))
    custom_production_brand = Column(String(32), nullable=False, server_default=text("''"))
    custom_production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_id = Column(Integer, nullable=False, index=True)
    production_brand = Column(String(32), nullable=False, server_default=text("''"))
    production_model = Column(String(64), nullable=False, server_default=text("''"))
    production_sku = Column(String(16), nullable=False, server_default=text("'Pcs'"))
    delivery_time = Column(String(128), nullable=False, server_default=text("''"))
    quantity = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_price = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    note = Column(String(64), nullable=False, server_default=text("''"))
    type_tax = Column(Integer, nullable=False, server_default=text("'1'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    company_address = Column(String(100), nullable=False, server_default=text("''"))
    company_site = Column(String(100), nullable=False, server_default=text("''"))
    company_tel = Column(String(100), nullable=False, server_default=text("''"))
    company_fax = Column(String(100), nullable=False, server_default=text("''"))
    company_email = Column(String(100), nullable=False, server_default=text("''"))
    company_type = Column(Integer, nullable=False, server_default=text("'0'"))
    owner_uid = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class SupplierContact(Base):
    __tablename__ = 'supplier_contact'

    id = Column(Integer, primary_key=True)
    cid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    name = Column(String(20), nullable=False, server_default=text("''"))
    salutation = Column(String(20), nullable=False, server_default=text("''"))
    mobile = Column(String(20), nullable=False, server_default=text("''"))
    tel = Column(String(20), nullable=False, server_default=text("''"))
    fax = Column(String(20), nullable=False, server_default=text("''"))
    email = Column(String(60), nullable=False, server_default=text("''"))
    department = Column(String(20), nullable=False, server_default=text("''"))
    address = Column(String(100), nullable=False, server_default=text("''"))
    note = Column(String(256), nullable=False, server_default=text("''"))
    status_default = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class SupplierInvoice(Base):
    __tablename__ = 'supplier_invoice'

    cid = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    company_tax_id = Column(String(20), nullable=False, server_default=text("''"))
    company_address = Column(String(100), nullable=False, server_default=text("''"))
    company_tel = Column(String(100), nullable=False, server_default=text("''"))
    company_bank_name = Column(String(100), nullable=False, server_default=text("''"))
    company_bank_account = Column(String(100), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20, u'utf8mb4_bin'), nullable=False, server_default=text("''"))
    salutation = Column(String(20), nullable=False, server_default=text("''"))
    mobile = Column(String(20), nullable=False, server_default=text("''"))
    tel = Column(String(20), nullable=False, server_default=text("''"))
    fax = Column(String(20), nullable=False, server_default=text("''"))
    email = Column(String(60), nullable=False, server_default=text("''"))
    role_id = Column(Integer, nullable=False, server_default=text("'0'"))
    parent_id = Column(Integer, nullable=False, server_default=text("'0'"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class UserAuth(Base):
    __tablename__ = 'user_auth'
    __table_args__ = (
        Index('type_auth', 'type_auth', 'auth_key', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    type_auth = Column(Integer, nullable=False, server_default=text("'0'"))
    auth_key = Column(String(60, u'utf8mb4_bin'), nullable=False, server_default=text("''"))
    auth_secret = Column(String(60, u'utf8mb4_bin'), nullable=False, server_default=text("''"))
    status_verified = Column(Integer, nullable=False, server_default=text("'0'"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, server_default=text("''"))
    address = Column(String(100), nullable=False, server_default=text("''"))
    linkman = Column(String(20), nullable=False, server_default=text("''"))
    tel = Column(String(20), nullable=False, server_default=text("''"))
    fax = Column(String(20), nullable=False, server_default=text("''"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
