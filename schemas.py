from pydantic import BaseModel, Field
from typing import Optional

class InventoryItemBase(BaseModel):
    """
    Base Pydantic model for common inventory item fields.
    Used for validation of name and description.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Name of the inventory item (required, unique).")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the item.")

class InventoryItemCreate(InventoryItemBase):
    """
    Pydantic model for creating a new inventory item.
    Inherits from InventoryItemBase and adds a default status.
    """
    status: bool = Field(True, description="Status of the item (True for active, False for inactive).")

class InventoryItemUpdate(InventoryItemBase):
    """
    Pydantic model for updating an existing inventory item.
    All fields are optional for updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="New name for the item (optional).")
    description: Optional[str] = Field(None, max_length=500, description="New description for the item (optional).")
    status: Optional[bool] = Field(None, description="New status for the item (optional).")

class InventoryItemResponse(InventoryItemBase):
    """
    Pydantic model for responding with an inventory item.
    Includes the 'id' and 'status' which are generated/managed by the database.
    """
    id: int = Field(..., description="Unique identifier of the item.")
    status: bool = Field(..., description="Current status of the item (active/inactive).")

    class Config:
        # This tells Pydantic to read data from ORM objects (like SQLAlchemy models).
        from_attributes = True # For Pydantic v2
        # orm_mode = True # For Pydantic v1
