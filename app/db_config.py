from models.base import Base
from models.user import User
from models.category import Category
from models.item import Item
from sqlalchemy import create_engine

engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)