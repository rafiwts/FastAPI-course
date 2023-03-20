from app import schema
from.database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Hello Worlds"
    assert res.status_code == 200 


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello11@gmail.com", "password": "password69"}
    )
    
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello11@gmail.com"
    assert res.status_code == 201