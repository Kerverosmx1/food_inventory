import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import app, Base, and get_db from your project modules
from main import app
from database import Base, get_db
from models import InventoryItem # Ensure models are imported so Base.metadata knows about them

# --- Test Database Setup ---
# Use a truly in-memory SQLite database for tests, ensuring a clean slate for each test.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(name="db")
def db_fixture():
    """
    Provides a clean database session for each test.
    Tables are created before each test and dropped after.
    """
    Base.metadata.create_all(bind=test_engine) # Create tables for the test database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine) # Drop tables to ensure clean state for next test

@pytest.fixture(name="client")
def client_fixture(db):
    """
    Provides a FastAPI test client with the overridden database dependency.
    This ensures tests use the in-memory test database.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close() # Close the session after the test
    
    # Override the get_db dependency in the main app
    app.dependency_overrides[get_db] = override_get_db
    
    # Use TestClient to make requests to the app
    with TestClient(app) as c:
        yield c
    
    # Clear the dependency override after the test
    app.dependency_overrides.clear()

# --- Unit Tests for CRUD Operations ---

def test_create_and_read_item(client):
    """
    Test creating an item and then reading it by ID and from the list.
    Covers POST /items/ and GET /items/{item_id} and GET /items/.
    """
    # Test Create (POST /items/)
    item_data = {"name": "Coffee Beans", "description": "Arabica dark roast", "status": True}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["name"] == "Coffee Beans"
    assert created_item["description"] == "Arabica dark roast"
    assert created_item["status"] is True
    assert "id" in created_item

    item_id = created_item["id"]

    # Test Read (single item - GET /items/{item_id})
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    read_item = response.json()
    assert read_item["id"] == item_id
    assert read_item["name"] == "Coffee Beans"
    assert read_item["description"] == "Arabica dark roast"
    assert read_item["status"] is True

    # Test Read (all items - GET /items/)
    response = client.get("/items/")
    assert response.status_code == 200
    read_items = response.json()
    assert len(read_items) == 1
    assert read_items[0]["name"] == "Coffee Beans"

def test_create_item_duplicate_name(client):
    """
    Test creating an item with a name that already exists (should result in 409 Conflict).
    """
    item_data = {"name": "Milk", "description": "Full fat milk"}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201

    response = client.post("/items/", json=item_data) # Attempt to create again with same name
    assert response.status_code == 409 # Conflict
    assert response.json()["detail"] == "Item with this name already exists"

def test_read_non_existent_item(client):
    """
    Test reading an item that does not exist (should result in 404 Not Found).
    """
    response = client.get("/items/999") # Assuming ID 999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item(client):
    """
    Test updating an existing item (PUT /items/{item_id}).
    """
    # Create an item first
    item_data = {"name": "Sugar", "description": "White granulated sugar"}
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Update the item's description and status
    update_data = {"description": "Brown sugar alternative", "status": False}
    update_response = client.put(f"/items/{item_id}", json=update_data)
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["id"] == item_id
    assert updated_item["name"] == "Sugar" # Name should remain unchanged if not provided in update_data
    assert updated_item["description"] == "Brown sugar alternative"
    assert updated_item["status"] is False

    # Verify the update by reading the item again
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    retrieved_item = get_response.json()
    assert retrieved_item["description"] == "Brown sugar alternative"
    assert retrieved_item["status"] is False

def test_update_non_existent_item(client):
    """
    Test updating an item that does not exist (should result in 404 Not Found).
    """
    update_data = {"name": "NonExistent", "description": "Should fail"}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item_duplicate_name_conflict(client):
    """
    Test updating an item's name to one that already exists for *another* item.
    """
    # Create two items
    item1_data = {"name": "Item A"}
    item2_data = {"name": "Item B"}
    
    resp1 = client.post("/items/", json=item1_data)
    assert resp1.status_code == 201
    item1_id = resp1.json()["id"]

    resp2 = client.post("/items/", json=item2_data)
    assert resp2.status_code == 201
    item2_id = resp2.json()["id"]

    # Try to update Item B's name to Item A's name
    update_data = {"name": "Item A"}
    response = client.put(f"/items/{item2_id}", json=update_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "Another item with this name already exists"

def test_delete_item(client):
    """
    Test deleting an existing item (DELETE /items/{item_id}).
    """
    # Create an item first
    item_data = {"name": "Bread", "description": "Whole wheat bread"}
    create_response = client.post("/items/", json=item_data)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204 # No Content

    # Verify deletion by trying to read the item again
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Item not found"

def test_delete_non_existent_item(client):
    """
    Test deleting an item that does not exist (should result in 404 Not Found).
    """
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
