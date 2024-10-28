from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os
import pytest
from app.config import settings
from app.database import get_db, Base
from fastapi.testclient import TestClient
from app.main import app
from app.routers import oauth2
from app import models

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_TEST_URL = os.getenv("SQLALCHEMY_DATABASE_TEST_URL")
engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()   # Fixture to get a Database Session
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()   # Fixture to get a TestClient instance (Unauthenticated)
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()   # Fixture to create a new user
def test_user2(client):
    user_data = {
        "email": "test2@xyz.com",
        "password": "test"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()   # Fixture to create a new user
def test_user(client):
    user_data = {
        "email": "test@xyz.com",
        "password": "test"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    return oauth2.create_access_token({"user_id":test_user['id']})
    
@pytest.fixture()   # Returns instance of TestClient (Authorized)
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}" 
    }
    
    return client


@pytest.fixture()
def test_posts(test_user,session,test_user2):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    },
    {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }
    ]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model,posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts