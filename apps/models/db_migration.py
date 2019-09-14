# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text
from apps.databases.db_migration import migration_db


Base = migration_db.Model
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict
Base.__bind_key__ = 'db_migration'


class Contrast(Base):
    __tablename__ = 'contrast'

    id = Column(Integer, primary_key=True)
    table_name = Column(String(32), nullable=False, server_default=text("''"))
    pk_source = Column(String(36), nullable=False, server_default=text("''"))
    pk_target = Column(Integer, nullable=False, server_default=text("'0'"))
    latest_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status_delete = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_time = Column(DateTime)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
