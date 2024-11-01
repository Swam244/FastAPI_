import os
import uvicorn
from app.config import settings

ssl_keyfile = settings.SERVER_KEY
ssl_certfile = settings.SSL_CERTFILE

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
        reload=True
    )
