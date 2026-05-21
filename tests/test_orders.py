from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_orders.main import app
from app_orders.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqllite:///./test_orders.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_threads": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db()
client = TestClient(app)

def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def create_user(email="user@email.com"):
    return client.post("/users/", json={
        "email": email,
        "full_name": "Test User",
        "age": 30
    })

def test_create_order_user():
    create_user()

    payload = {
        "user_id": 1,
        "total_amount": 80.60
    }

    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == 1
    assert data["total_amount"] == 80.60
    assert data["status"] == "pending"

def test_create_order_invalid_user():
    payload = {
        "user_id": 999,
        "total_amount": 50
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 404

def test_create_order_invalid_amount():
    payload = {
        "user_id": 1,
        "total_amount": -10
    }

    response = client.post("/orders/", json=payload)
    assert response.status_code == 400


def test_get_order():
    response =  client.get("/orders/1")

    assert response.status_code == 200
    assert  response.json()["id"] == 1

def test_get_order_not_found():
    response = client.get("/orders/999")
    assert  response.status_code == 404


def test_update_status_success():
    response =  client.put("/orders/1", json={"status": "paid"})
    assert response.status_code == 200
    assert response.json()["status"] == "paid"

def test_update_status_invalid_transition():
    response =  client.patch("/orders/1/status", json={"status": "pending"})
    assert response.status_code == 400

def test_update_amount_forbidden_for_paid():
    response = client.patch("/orders/1/amount", json={"total_amount": 200})
    assert response.status_code == 400


def test_create_second_order_for_filters():
    client.post("/orders/", json={"user_id": 1, "total_amount": 20})
    client.post("/orders/", json={"user_id": 1, "total_amount": 200})
    client.post("/orders/", json={"user_id": 1, "total_amount": 300})


def test_list_order_pagination():
    response =  client.get("/orders?page=1&page_size=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_list_order_filter_by_amount():
    response = client.get("/orders?amount_min=250")
    assert response.status_code == 200
    data = response.json()
    assert all(float(o["total_amount"]) >= 250 for o in data)

def test_delete_order_forbidden_for_paid():
    response = client.delete("/orders/1")
    assert response.status_code == 400


def test_delete_order_success():
    response = client.delete("/orders/2")
    assert response.status_code == 204

    response = client.get("/orders/2")
    assert response.status_code == 404




