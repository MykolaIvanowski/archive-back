import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_products.main import app
from app_products.db.database import Base, get_db


# -------------------------
# TEST DATABASE (SQLite)
# -------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_products.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_product_success():
    payload = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 1200.50,
        "in_stock": True
    }

    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Laptop"
    assert data["category"] == "Electronics"
    assert float(data["price"]) == 1200.50
    assert data["in_stock"] is True


def test_create_product_duplicate_name():
    payload = {
        "name": "Laptop",
        "category": "Electronics",
        "price": 900,
        "in_stock": True
    }

    response = client.post("/products/", json=payload)
    assert response.status_code == 400
    assert "exists" in response.json()["detail"]


def test_create_product_invalid_price():
    payload = {
        "name": "Cheap Item",
        "category": "Misc",
        "price": -5,
        "in_stock": True
    }

    response = client.post("/products/", json=payload)
    assert response.status_code == 400


def test_get_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404


def test_update_product_success():
    payload = {
        "name": "Laptop Pro",
        "category": "Electronics",
        "price": 1500,
        "in_stock": False
    }

    response = client.put("/products/1", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Laptop Pro"
    assert float(data["price"]) == 1500
    assert data["in_stock"] is False


def test_patch_product_success():
    payload = {
        "price": 1600
    }

    response = client.patch("/products/1", json=payload)
    assert response.status_code == 200
    assert float(response.json()["price"]) == 1600


def test_patch_product_invalid_price():
    payload = {
        "price": -10
    }

    response = client.patch("/products/1", json=payload)
    assert response.status_code == 400


def test_create_more_products_for_filters():
    client.post("/products/", json={
        "name": "Phone",
        "category": "Electronics",
        "price": 800,
        "in_stock": True
    })

    client.post("/products/", json={
        "name": "Shoes",
        "category": "Fashion",
        "price": 120,
        "in_stock": False
    })

    client.post("/products/", json={
        "name": "T-Shirt",
        "category": "Fashion",
        "price": 25,
        "in_stock": True
    })


def test_list_products_pagination():
    response = client.get("/products?page=1&page_size=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_products_filter_by_category():
    response = client.get("/products?category=Fashion")
    assert response.status_code == 200
    data = response.json()
    assert all(p["category"] == "Fashion" for p in data)


def test_list_products_filter_by_price_range():
    response = client.get("/products?price_min=100&price_max=900")
    assert response.status_code == 200
    data = response.json()
    assert all(100 <= float(p["price"]) <= 900 for p in data)


def test_list_products_filter_by_name_contains():
    response = client.get("/products?name=top")
    assert response.status_code == 200
    data = response.json()
    assert any("top" in p["name"].lower() for p in data)


def test_delete_product_success():
    response = client.delete("/products/1")
    assert response.status_code == 204

    # ensure deleted
    response = client.get("/products/1")
    assert response.status_code == 404