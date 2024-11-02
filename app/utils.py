from passlib.context import CryptContext
from fastapi import Request,HTTPException

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password : str):
    return pwd_context.hash(password)

def verifyPass(plain_pass,hashed_pass):
    return pwd_context.verify(plain_pass,hashed_pass)

def csrf_protect(request: Request):
    csrf_token = request.headers.get("X-CSRF-Token") or request.query_params.get("csrf_token")
    print(csrf_token)
    print(request.session.get("csrf_token"))
    if not csrf_token or csrf_token != request.session.get("csrf_token"):
        raise HTTPException(status_code=403, detail="CSRF token verification failed")