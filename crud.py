from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import InventoryItem
from .schemas import InventoryItemCreate, InventoryItemUpdate

def get_item(db: Session, item_id: int):
    """Retrieve a single inventory item by its ID."""
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()

def get_item_by_name(db: Session, name: str):
    """Retrieve a single inventory item by its name."""
    return db.query(InventoryItem).filter(InventoryItem.name == name).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of inventory items with pagination."""
    return db.query(InventoryItem).offset(skip).limit(limit).all()

def create_item(db: Session, item: InventoryItemCreate):
    """
    Create a new inventory item.
    Returns the created item or None if a conflict (e.g., duplicate name) occurs.
    """
    db_item = InventoryItem(
        name=item.name,
        description=item.description,
        status=item.status
    )
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item) # Refresh to get the generated ID
        return db_item
    except IntegrityError:
        db.rollback() # Rollback in case of unique constraint violation
        return None

def update_item(db: Session, item_id: int, item: InventoryItemUpdate):
    """
    Update an existing inventory item.
    Returns the updated item or None if not found or a conflict occurs.
    """
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if db_item:
        # Use model_dump(exclude_unset=True) to only update fields that were provided in the request
        update_data = item.model_dump(exclude_unset=True) # Pydantic v2
        for key, value in update_data.items():
            setattr(db_item, key, value)
        try:
            db.add(db_item) # Add to session to track changes
            db.commit()
            db.refresh(db_item)
            return db_item
        except IntegrityError:
            db.rollback() # Rollback in case of unique constraint violation
            return None
    return None

def delete_item(db: Session, item_id: int):
    """
    Delete an inventory item.
    Returns the deleted item or None if not found.
    """
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
