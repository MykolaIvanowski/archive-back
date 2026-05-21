import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_users.main import app
from app_users.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSessionLocal()
    try :
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.dropall(bins=engine)
    Base.matadata.create_all(bind=engine)
    yield
    Base.matadata.drop_all(bind=engine)

def test_create_user():
    payload = {
        'email': 'newtest@emailtest.com',
        'first_name': 'Jon',
        'last_name': 'Smith',
        'age': 28
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == payload['email']
    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert data['age'] == payload['age']


def test_create_user_duplicate_email():
    payload = {
        'email': 'newtest@emailtest.com',
        'first_name': 'Jon',
        'last_name': 'Smith',
        'age': 30
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 400
    assert "exists" in response.json()['detail']

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'newtest@emailtest.com'

def test_get_user_not_found():
    response = client.get("/users/10000")
    assert response.status_code == 404


def test_list_user_pagination():
    for i in range(2,12):
        client.post("/users", json={
            "email": f"user{i}@example.com",
            "first_name": f"Jon{i}",
            "last_name": f"Smith{i}",
            "age": 29+i
        })

    response = client.get("/users?page=1&page_size=5")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_list_users_filter_by_email():
    response = client.get("/users?email=newtest@emailtest.com")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1

def test_update_user():
    payload = {
        'email': "newtest@emailtest.com",
        'first_name': "Ken",
        'last_name': 'Miller',
        "age": 30
    }

    response = client.put("/users/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == payload['email']
    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert data['age'] == payload['age']


def test_patch_user():
    payload = {
        'first_name': "Adam",
        'last_name': 'Wonka'
    }

    response = client.patch("/users/1", json=payload)
    assert  response.status_code == 200
    data = response.json()

    assert data['first_name'] == 'Adam'
    assert data['last_name'] == 'Wonka'

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200

    response = client.get("/users/1")
    assert response.status_code == 404


