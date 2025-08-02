from sqlalchemy import Boolean, Column, Integer, String, Text
from .database import Base # Import Base from database.py

class InventoryItem(Base):
    """
    SQLAlchemy model for an inventory item.
    Maps to the 'inventory_items' table in the database.
    """
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True, nullable=False) # True for active, False for inactive