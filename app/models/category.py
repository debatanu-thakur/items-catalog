import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy import SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from .base import Base
from .user import User


class Category(Base):

    __tablename__ = "catalog_category"
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = Column(DateTime, nullable=True,
                          default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    items = relationship("Item", order_by="Item.id",
                         collection_class=ordering_list('id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'createdAt': self.created_at,
            'lastUpdated': self.last_updated,
            'items': [item.serialize for item in self.items]
        }

