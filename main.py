from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from . import crud, models, schemas
from .database import engine, get_db # Import engine and get_db from database.py

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Food & Beverage Inventory API",
    description="A simple REST API for managing food and beverage inventory items.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
def on_startup():
    """
    Event handler that runs when the FastAPI application starts up.
    It creates all database tables if they don't already exist.
    """
    logger.info("Application startup: Creating database tables...")
    # Ensure models.Base is the same Base object from database.py
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created (if not existing).")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check API status.
    """
    return {"message": "Welcome to the Food & Beverage Inventory API! Visit /docs for API documentation."}

@app.post("/items/", response_model=schemas.InventoryItemResponse, status_code=status.HTTP_201_CREATED, tags=["Inventory Items"])
def create_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    """
    **Create a new inventory item.**
    - **name**: Required, unique string (min 1, max 100 chars).
    - **description**: Optional string (max 500 chars).
    - **status**: Optional boolean (default: `True` for active).
    """
    logger.info(f"Attempting to create item: {item.name}")
    
    # Check for duplicate name before attempting creation
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        logger.warning(f"Item with name '{item.name}' already exists. Conflict (409).")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item with this name already exists")
    
    created_item = crud.create_item(db=db, item=item)
    
    # This case should ideally be caught by the name check, but as a fallback for other DB errors
    if not created_item:
        logger.error(f"Failed to create item {item.name} due to an unexpected database error (500).")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create item due to an unexpected error.")
    
    logger.info(f"Successfully created item with ID: {created_item.id}")
    return created_item

@app.get("/items/", response_model=list[schemas.InventoryItemResponse], tags=["Inventory Items"])
def read_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    **Retrieve a list of all inventory items.**
    - **skip**: Number of items to skip (for pagination, default: 0).
    - **limit**: Maximum number of items to return (default: 100).
    """
    logger.info(f"Fetching inventory items (skip={skip}, limit={limit}).")
    items = crud.get_items(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(items)} items.")
    return items

@app.get("/items/{item_id}", response_model=schemas.InventoryItemResponse, tags=["Inventory Items"])
def read_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """
    **Retrieve a single inventory item by its ID.**
    - **item_id**: The unique integer identifier of the item.
    """
    logger.info(f"Fetching item with ID: {item_id}")
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning(f"Item with ID {item_id} not found (404).")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info(f"Successfully retrieved item with ID: {item_id}")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.InventoryItemResponse, tags=["Inventory Items"])
def update_inventory_item(item_id: int, item: schemas.InventoryItemUpdate, db: Session = Depends(get_db)):
    """
    **Update an existing inventory item.**
    - **item_id**: The unique integer identifier of the item to update.
    - **name**: Optional, new name for the item (min 1, max 100 chars).
    - **description**: Optional, new description for the item (max 500 chars).
    - **status**: Optional, new status (active/inactive) for the item.
    """
    logger.info(f"Attempting to update item with ID: {item_id}")
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        logger.warning(f"Item with ID {item_id} not found for update (404).")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    # Check for name conflict if name is being updated to an existing name of another item
    if item.name is not None and item.name != db_item.name:
        existing_item_with_name = crud.get_item_by_name(db, name=item.name)
        if existing_item_with_name and existing_item_with_name.id != item_id:
            logger.warning(f"Update failed: Item with name '{item.name}' already exists for another item (409).")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Another item with this name already exists")

    updated_item = crud.update_item(db=db, item_id=item_id, item=item)
    
    # This should not happen if item_id is found and name conflict is handled
    if not updated_item:
        logger.error(f"Failed to update item {item_id} due to an unexpected database error (500).")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update item due to an unexpected error.")
    
    logger.info(f"Successfully updated item with ID: {item_id}")
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inventory Items"])
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """
    **Delete an inventory item by its ID.**
    - **item_id**: The unique integer identifier of the item to delete.
    """
    logger.info(f"Attempting to delete item with ID: {item_id}")
    deleted_item = crud.delete_item(db, item_id=item_id)
    if deleted_item is None:
        logger.warning(f"Item with ID {item_id} not found for deletion (404).")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info(f"Successfully deleted item with ID: {item_id}")
    return None # Return None for 204 No Content
