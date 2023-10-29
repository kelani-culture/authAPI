from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, sql, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

"""
create models for our application
"""

class Users(Base):
    __tablename__  = 'users'
    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    products = relationship('Product')
    username=Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, server_default=sql.false())
    is_superuser = Column(Boolean, nullable=False, server_default=sql.false())
    is_admin = Column(Boolean, nullable=False, server_default=sql.false())
    is_verified = Column(Boolean, nullable=False, server_default=sql.false())


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, server_default='0')
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text("now()"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    seller = relationship("Users")