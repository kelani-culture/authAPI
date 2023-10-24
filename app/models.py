from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
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


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, server_default='0')
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text("now()"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))