
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_article.main import app
from app_article.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_articles.db"

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

def test_create_article():
    payload = {
        "title": "First Article",
        "content": "Hello world"
    }
    response = client.post("/articles", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "First Article"
    assert data["content"] == "Hello world"
    assert data["version"] == 1

def test_get_article():
    response = client.get("/articles/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "First Article"


def test_update_article_success():
    response = client.put("/articles/1").json()
    version  = response["version"]
    payload = {
        "title": "Updated Title",
        "content": "Updated content",
        "version": version
    }

    response = client.put("/articles/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    assert data["version"] == version + 1


def test_get_article_version_conflict():
    payload = {
        "title": "Conflict Title",
        "content": "Conflict content",
        "version": 1   # outdated
    }
    response = client.put("/articles/1", json=payload)
    assert response.status_code == 409
    assert "version mismatched" in response.json()["detail"]


def test_patch_article_success():
    article = client.patch("/articles/1").json()
    version = article["version"]
    payload = {
        "title": "Patched Title",
        "version": version
    }
    response = client.patch("/articles/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Patched Title"
    assert data["content"] == "Patched content"
    assert data["version"] == version + 1


def test_patch_article_version_conflict():
    payload = {
        "content": "Should fail",
        "version": 1  # outdated
    }
    response = client.patch("/articles/1", json=payload)
    assert response.status_code == 409


def test_list_articles():
    response = client.get("/articles?page=1&page_size=10")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_delete_article():
    response = client.delete("/articles/1")
    assert response.status_code == 204

    response = client.get("/articles/1")
    assert response.status_code == 404


def test_restore_article():
    response = client.post("/articles/1/restore")
    assert response.status_code == 200
    assert response.json()["delete_at"] is None
    response = client.get("/articles/1")
    assert response.status_code == 200

def test_audit_log_entries():
    response = client.get("/articles/1/audit-log")
    assert response.status_code == 200

    logs = response.json()
    assert len(logs) >= 4

    actions = [log["action"] for log in logs]
    assert "create" in actions
    assert "update" in actions
    assert "delete" in actions
    assert "restore" in actions
