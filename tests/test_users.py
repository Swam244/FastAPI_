from app.main import app
from app.schemas import *
from app.config import settings
from jose import jwt
import pytest

def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "test@xyz.com", "password": "test"}
    )
    new_user = UserResponse(**res.json())
    assert new_user.email == "test@xyz.com"
    assert res.status_code == 201


def test_login_user(client,test_user):
    res = client.post("/login/",
        data={
            "username": test_user['email'],
            "password": test_user['password']
            }
    )
    login_res = Token(**res.json())
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    payload = jwt.decode(login_res.access_token,SECRET_KEY,algorithms=[ALGORITHM])
    id = payload.get("user_id")
    
    assert res.status_code == 200
    assert login_res.token_type == 'bearer'
    assert id == test_user['id']




@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@xyz.com','test',403),
    ('test@xyz.com','wrongpassword',403),
    ('wrongemail@xyz.com','wrongpassword',403),
    (None,'test',422),
    ('test@xyz.com',None,422)
])
def test_incorrect_login(client,test_user,email,password,status_code):
    res = client.post("/login/",
        data={
            "username": email,
            "password": password
            }
    )
    
    assert res.status_code == status_code
    
