import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings
from app.main import app
from app.database import get_db, Base 
from app.authentication import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_userame}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


@pytest.fixture# as a result the tables will not be dropped until the end of the session
def session():                  # so that we can login a user
    Base.metadata.drop_all(bind=engine) # deletes everything before running
    Base.metadata.create_all(bind=engine) # runs our code before we run our test - it creates tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):  # db will be passed as a session parameter
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app) #new test client - we have an access to databases and client (we can make queries)


@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com",
                 "password": "password123"
                }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "rafa@gmail.com",
                 "password": "password123"
                }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first title",
        "content": "first content",
        "user_id": test_user['id']},
        {"title": "second title",
        "content": "second content",
        "user_id": test_user['id']},
        {"title": "third title",
         "content": "third content",
         "user_id": test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="second title", content="second content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts