import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_debate.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    assert client.get("/health").status_code == 200

def test_create_debate(client):
    r = client.post("/api/debates/", json={"topic": "AI will transform the economy within a decade", "rounds": 1})
    assert r.status_code == 201

def test_invalid_topic(client):
    assert client.post("/api/debates/", json={"topic": "short", "rounds": 1}).status_code == 422

def test_list_empty(client):
    assert client.get("/api/debates/").json() == []

def test_get_not_found(client):
    assert client.get("/api/debates/999").status_code == 404

def test_delete_debate(client):
    r = client.post("/api/debates/", json={"topic": "Universal basic income would help society greatly", "rounds": 1})
    did = r.json()["id"]
    assert client.delete(f"/api/debates/{did}").status_code == 204
    assert client.get(f"/api/debates/{did}").status_code == 404

def test_score_endpoint(client):
    r = client.post("/api/debates/score", json={"argument_text": "The evidence clearly supports this position with multiple peer-reviewed studies confirming the hypothesis.", "topic": "AI safety research", "stance": "pro"})
    assert r.status_code == 200
    assert r.json()["label"] in ("weak", "moderate", "strong")

def test_stats(client):
    r = client.get("/api/debates/stats/summary")
    assert r.status_code == 200
    assert r.json()["total_debates"] == 0
