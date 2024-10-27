from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv()

# FORMAT postgres://<username>:<password>@ip:host/<database_name>
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# while True:
#     try:
#         conn = psycopg2.connect(host=os.getenv('DATABASE_HOST'), database=os.getenv("DATABASE_NAME"), user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"),
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(colored("[ DATABASE CONNECTION SUCCESSFULL ]", 'green'))
#         break

#     except Exception as err:
#         print(colored("[ CONNECTION TO DATABASE FAILED ]", 'red'))
#         print(colored("[ ERROR ] : "+str(err), 'red'))
#         time.sleep(2)

