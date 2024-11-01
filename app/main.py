from fastapi import FastAPI,Depends
from . import models
from .database import engine
from .routers import users,posts,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine,checkfirst=True)  # Tables are created only when they do not exist.

SERVER_KEY = settings.SERVER_KEY
SSL_CERTFILE = settings.SSL_CERTFILE

app = FastAPI(ssl_keyfile = SERVER_KEY ,ssl_certfile= SSL_CERTFILE)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def root():
    return {"Message": "Hello World"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)




