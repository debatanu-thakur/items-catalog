import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy import SmallInteger
from sqlalchemy.orm import relationship
from .category import Category
from .base import Base


class Item(Base):
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    last_updated = Column(DateTime, nullable=True,
                          default=datetime.datetime.now,
                          onupdate=datetime.datetime.now)
    category_id = Column(Integer, ForeignKey("catalog_category.id"))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'isDeleted': self.is_deleted,
            'createdAt': self.created_at,
            'lastUpdated': self.last_updated,
            'categoryId': self.category_id
        }
